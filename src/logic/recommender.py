from src.data.models import User, Course

def get_recommendations(user: User):
    # This is a placeholder for the actual recommendation logic.
    # In a real system, this would use the user's GPA, courses,
    # and potentially other factors to recommend courses.
    
    if user.gpa and user.gpa >= 3.5:
        return ["Advanced Algorithms", "Machine Learning", "Deep Learning"]
    elif user.gpa and user.gpa >= 2.5:
        return ["Data Structures II", "Database Systems", "Operating Systems"]
    else:
        return ["Introduction to Programming II", "Discrete Mathematics", "Computer Architecture"]
