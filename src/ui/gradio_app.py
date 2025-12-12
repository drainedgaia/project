import gradio as gr
from src.data.models import User
from src.utils.validation import validate_email, validate_gpa
from src.logic.recommender import get_recommendations

current_user = None

def user_info_submit(first_name, last_name, email):
    global current_user
    if not first_name or not last_name or not email:
        gr.Warning("Please fill in all fields.")
        return gr.update(visible=True), gr.update(visible=False)
    if not validate_email(email):
        gr.Warning("Invalid email format.")
        return gr.update(visible=True), gr.update(visible=False)
    
    current_user = User(first_name, last_name, email, 0.0, [])
    return gr.update(visible=False), gr.update(visible=True)

def academic_info_submit(
    gpa_str, age, gender, ethnicity, parental_education, study_time_weekly, 
    absences, tutoring, parental_support, extracurricular, sports, music, volunteering
):
    global current_user
    if not current_user:
        gr.Warning("Please submit user information first.")
        return "", "", gr.update(visible=True), gr.update(visible=False)
    
    if not validate_gpa(gpa_str):
        gr.Warning('Invalid GPA. Please enter a value between 0.0 and 4.0.')
        return "", "", gr.update(visible=True), gr.update(visible=False)
    
    current_user.gpa = float(gpa_str)

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
        return "", "", gr.update(visible=True), gr.update(visible=False)

    recommendations = get_recommendations(
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
        gpa=current_user.gpa,
    )

    confirmation_message = f"""
    **User Information:**
    Name: {current_user.first_name} {current_user.last_name}
    Email: {current_user.email}

    **Academic & Personal Information:**
    GPA: {current_user.gpa}
    Age: {age}
    Study Time Weekly: {study_time_weekly} hours
    Absences: {absences} days
    """
    
    recommendation_message = "\n**Recommended Courses:**\n" + "\n".join([f"- {rec}" for rec in recommendations])

    return confirmation_message, recommendation_message, gr.update(visible=False), gr.update(visible=True)

with gr.Blocks() as app:
    gr.Markdown("# Student Recommendation System")

    with gr.Column(visible=True) as user_info_page:
        gr.Markdown("## 1. User Information")
        first_name_input = gr.Textbox(label="First Name")
        last_name_input = gr.Textbox(label="Last Name")
        email_input = gr.Textbox(label="Email")
        user_info_button = gr.Button("Next")

    with gr.Column(visible=False) as academic_info_page:
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
        recommendation_display = gr.Markdown()
        
    user_info_button.click(
        user_info_submit,
        inputs=[first_name_input, last_name_input, email_input],
        outputs=[user_info_page, academic_info_page]
    )

    academic_info_button.click(
        academic_info_submit,
        inputs=[
            gpa_input, age_input, gender_input, ethnicity_input, parental_education_input,
            study_time_weekly_input, absences_input, tutoring_input, parental_support_input,
            extracurricular_input, sports_input, music_input, volunteering_input
        ],
        outputs=[confirmation_display, recommendation_display, academic_info_page, recommendation_page]
    )

if __name__ == "__main__":
    app.launch()