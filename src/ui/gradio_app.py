
import gradio as gr
import pandas as pd
from src.data.database import init_db, SessionLocal
from src.logic.auth import authenticate_user, create_user
from src.data.models import User
from src.utils.validation import validate_email, validate_gpa
from src.logic.recommender import get_recommendations

def app():
    init_db()

    with gr.Blocks() as app:
        user_state = gr.State(None)
        
        with gr.Column(visible=True) as login_view:
            with gr.Tabs():
                with gr.TabItem("Login"):
                    email_input = gr.Textbox(label="Email")
                    password_input = gr.Textbox(label="Password", type="password")
                    login_button = gr.Button("Login")
                with gr.TabItem("Signup"):
                    signup_first_name = gr.Textbox(label="First Name")
                    signup_last_name = gr.Textbox(label="Last Name")
                    signup_email = gr.Textbox(label="Email")
                    signup_password = gr.Textbox(label="Password", type="password")
                    signup_button = gr.Button("Signup")

        with gr.Column(visible=False) as main_app_view:
            gr.Markdown("# Student Recommendation System")

            with gr.Column(visible=True) as academic_info_page:
                gr.Markdown("## 2. Academic and Personal Information")
                
                with gr.Row():
                    gpa_input = gr.Number(label="Previous GPA (0.0-4.0)", value=3.0)
                    age_input = gr.Number(label="Age", value=16)
                    study_time_weekly_input = gr.Slider(label="Study Time Weekly (hours)", minimum=0, maximum=20, value=10)
                
                with gr.Row():
                    absences_input = gr.Slider(label="Absences (days)", minimum=0, maximum=30, value=5)
                    parental_education_input = gr.Radio(label="Parental Education", choices=[("None", 0), ("High School", 1), ("Some College", 2), ("Bachelor's", 3), ("Higher", 4)], value=2)
                    parental_support_input = gr.Radio(label="Parental Support", choices=[("None", 0), ("Low", 1), ("Moderate", 2), ("High", 3), ("Very High", 4)], value=2)

                with gr.Row():
                    gender_input = gr.Radio(label="Gender", choices=[("Female", 0), ("Male", 1)], value=0)
                    ethnicity_input = gr.Radio(label="Ethnicity", choices=[("Caucasian", 0), ("African American", 1), ("Asian", 2), ("Other", 3)], value=0)
                    tutoring_input = gr.Radio(label="Tutoring", choices=[("No", 0), ("Yes", 1)], value=0)

                with gr.Row():
                    extracurricular_input = gr.Radio(label="Extracurricular Activities", choices=[("No", 0), ("Yes", 1)], value=0)
                    sports_input = gr.Radio(label="Sports", choices=[("No", 0), ("Yes", 1)], value=0)
                    music_input = gr.Radio(label="Music", choices=[("No", 0), ("Yes", 1)], value=0)
                    volunteering_input = gr.Radio(label="Volunteering", choices=[("No", 0), ("Yes", 1)], value=0)

                academic_info_button = gr.Button("Submit")

            with gr.Column(visible=False) as recommendation_page:
                gr.Markdown("## 3. Recommendations")
                confirmation_display = gr.Markdown()
                estimated_grade_display = gr.Markdown()
                recommendation_display = gr.DataFrame()
                
        def academic_info_submit(user, gpa_str, age, gender, ethnicity, parental_education, study_time_weekly, 
            absences, tutoring, parental_support, extracurricular, sports, music, volunteering):
            
            if not validate_gpa(gpa_str):
                gr.Warning('Invalid GPA. Please enter a value between 0.0 and 4.0.')
                return gr.update(), gr.update(), gr.update(), gr.update(visible=True), gr.update(visible=False)
            
            user.gpa = float(gpa_str)

            # Convert inputs to the correct types
            try:
                age = int(age)
                gender = int(gender)
                ethnicity = int(ethnicity)
                parental_education = int(parental_education)
                study_time_weekly = float(study_time_weekly)
                absences = int(absences)
                tutoring = int(tutoring)
                parental_support = int(parental_support)
                extracurricular = int(extracurricular)
                sports = int(sports)
                music = int(music)
                volunteering = int(volunteering)
            except (ValueError, TypeError):
                gr.Warning("Please ensure all fields are filled correctly.")
                return gr.update(), gr.update(), gr.update(), gr.update(visible=True), gr.update(visible=False)

            grade_class, recommended_courses = get_recommendations(
                age=age,
                gender=gender,
                ethnicity=ethnicity,
                parental_education=parental_education,
                study_time_weekly=study_time_weekly,
                absences=absences,
                tutoring=tutoring,
                parental_support=parental_support,
                extracurricular=extracurricular,
                sports=sports,
                music=music,
                volunteering=volunteering,
                gpa=user.gpa,
            )

            confirmation_message = f"""
            **User Information:**
            Name: {user.first_name} {user.last_name}
            Email: {user.email}

            **Academic & Personal Information:**
            GPA: {user.gpa}
            Age: {age}
            Study Time Weekly: {study_time_weekly} hours
            Absences: {absences} days
            """
            
            recommendations_df = pd.DataFrame(recommended_courses)
            estimated_grade = f"**Estimated Grade:** {grade_class}"

            return gr.update(value=confirmation_message), gr.update(value=estimated_grade), gr.update(value=recommendations_df), gr.update(visible=False), gr.update(visible=True)

        def login(email, password):
            if not email or not password:
                gr.Warning("Please fill in all fields.")
                return None, gr.update(visible=True), gr.update(visible=False)
            
            db = SessionLocal()
            user = authenticate_user(db, email, password)
            db.close()

            if user:
                gr.Info("Login successful!")
                return user, gr.update(visible=False), gr.update(visible=True)
            else:
                gr.Warning("Invalid email or password.")
                return None, gr.update(visible=True), gr.update(visible=False)

        def signup(first_name, last_name, email, password):
            if not all([first_name, last_name, email, password]):
                gr.Warning("Please fill in all fields.")
                return
            
            db = SessionLocal()
            user = db.query(User).filter(User.email == email).first()
            if user:
                gr.Warning("User with this email already exists.")
                db.close()
                return
            
            create_user(db, first_name, last_name, email, password)
            db.close()
            gr.Info("Signup successful! You can now login.")


        login_button.click(login, inputs=[email_input, password_input], outputs=[user_state, login_view, main_app_view])
        signup_button.click(signup, inputs=[signup_first_name, signup_last_name, signup_email, signup_password], outputs=[])
        
        academic_info_button.click(
            academic_info_submit,
            inputs=[
                user_state, gpa_input, age_input, gender_input, ethnicity_input, parental_education_input,
                study_time_weekly_input, absences_input, tutoring_input, parental_support_input,
                extracurricular_input, sports_input, music_input, volunteering_input
            ],
            outputs=[confirmation_display, estimated_grade_display, recommendation_display, academic_info_page, recommendation_page]
        )

    return app
