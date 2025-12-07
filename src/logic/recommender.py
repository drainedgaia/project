import random
import time

from src.data.models import User, Course

def get_recommendations(user: User):
    # This is a placeholder for the actual recommendation logic.
    # In a real system, this would use the user's GPA, courses,
    # and potentially other factors to recommend courses.

    # time.sleep(5)

    st_course = ["Advanced Algorithms", "Machine Learning", "Deep Learning"]
    nd_courses = ["Data Structures II", "Database Systems", "Operating Systems"]
    rd_courses = ["Introduction to Programming II", "Discrete Mathematics", "Computer Architecture"]

    if user.gpa and user.gpa >= 3.5:
        random.shuffle(st_course)
        return st_course
    elif user.gpa and user.gpa >= 2.5:
        random.shuffle(nd_courses)
        return nd_courses
    else:
        random.shuffle(rd_courses)
        return rd_courses
