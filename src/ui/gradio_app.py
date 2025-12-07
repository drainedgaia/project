import gradio as gr
from src.data.models import User, Course
from src.utils.validation import validate_email, validate_gpa
from src.logic.recommender import get_recommendations

current_user = None

def user_info_submit(first_name, last_name, email):
    global current_user
    if not first_name or not last_name or not email:
        return "Please fill in all fields.", gr.update(visible=True), gr.update(visible=False)
    if not validate_email(email):
        return "Invalid email format.", gr.update(visible=True), gr.update(visible=False)
    
    current_user = User(first_name, last_name, email)
    return "User info submitted successfully!", gr.update(visible=False), gr.update(visible=True)

def add_course(course_name, course_grade, current_courses):
    if not course_name or not course_grade:
        return current_courses, "Please enter both course name and grade.", gr.update(value=""), gr.update(value="")
    
    current_courses.append(Course(course_name, course_grade))
    course_list_str = "Added Courses:\n" + "\n".join([f"- {c.name}: {c.grade}" for c in current_courses])
    return current_courses, course_list_str, gr.update(value=""), gr.update(value="")

def academic_info_submit(gpa_str, current_courses):
    global current_user
    if not current_user:
        return "Please submit user information first.", gr.update(visible=True), gr.update(visible=False)
    
    if not validate_gpa(gpa_str):
        gr.Warning('Invalid GPA. Please enter a value between 0.0 and 4.0.')
        return "", gr.update(visible=True), gr.update(visible=False), gr.update(visible=False)
    
    current_user.gpa = float(gpa_str)
    current_user.courses = current_courses

    if len(current_user.courses) < 5:
        gr.Warning('Please Provide at least 5 previous courses.')
        return "", gr.update(visible=True), gr.update(visible=False), gr.update(visible=False)
    
    recommendations = get_recommendations(current_user)

    confirmation_message = f"""
    **User Information:**
    Name: {current_user.first_name} {current_user.last_name}
    Email: {current_user.email}

    **Academic Information:**
    GPA: {current_user.gpa}
    Courses:
    """
    for course in current_user.courses:
        confirmation_message += f"- {course.name}: {course.grade}\n"
    
    recommendation_message = "\n**Recommended Courses:**\n" + "\n".join([f"- {rec}" for rec in recommendations])

    return confirmation_message, recommendation_message, gr.update(visible=False), gr.update(visible=True)

with gr.Blocks() as app:
    gr.Markdown("# Student Recommendation System")

    # State to store courses
    courses_state = gr.State([])

    with gr.Column(visible=True) as user_info_page:
        gr.Markdown("## 1. User Information")
        first_name_input = gr.Textbox(label="First Name")
        last_name_input = gr.Textbox(label="Last Name")
        email_input = gr.Textbox(label="Email")
        user_info_output = gr.Textbox(label="Status", interactive=False)
        user_info_button = gr.Button("Next")

    with gr.Column(visible=False) as academic_info_page:
        gr.Markdown("## 2. Academic Information")
        gpa_input = gr.Textbox(label="Previous GPA (0.0-4.0)")
        
        gr.Markdown("### Add Courses")
        with gr.Row():
            course_name_input = gr.Textbox(label="Course Name")
            course_grade_input = gr.Textbox(label="Course Grade")
            add_course_button = gr.Button("Add Course")
        
        added_courses_display = gr.Markdown("Added Courses:")
        academic_info_output = gr.Textbox(label="Status", interactive=False)
        academic_info_button = gr.Button("Submit")

    with gr.Column(visible=False) as recommendation_page:
        gr.Markdown("## 3. Recommendations")
        confirmation_display = gr.Markdown()
        recommendation_display = gr.Markdown()
        
    user_info_button.click(
        user_info_submit,
        inputs=[first_name_input, last_name_input, email_input],
        outputs=[user_info_output, user_info_page, academic_info_page]
    )

    add_course_button.click(
        add_course,
        inputs=[course_name_input, course_grade_input, courses_state],
        outputs=[courses_state, added_courses_display, course_name_input, course_grade_input]
    )

    academic_info_button.click(
        academic_info_submit,
        inputs=[gpa_input, courses_state],
        outputs=[confirmation_display, recommendation_display, academic_info_page, recommendation_page]
    )

if __name__ == "__main__":
    app.launch()
