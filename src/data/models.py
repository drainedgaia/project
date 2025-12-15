from src.data.database import User

class Course:
    def __init__(self, course_id, course_name, course_description):
        self.course_id = course_id
        self.course_name = course_name
        self.course_description = course_description

    def __str__(self):
        return f"Course(course_id={self.course_id}, course_name={self.course_name})"