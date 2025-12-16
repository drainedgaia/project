
import joblib
import pandas as pd
import numpy as np
import os
import random

# Dummy course catalog
COURSE_CATALOG = {
    "Advanced Algorithms": {"code": "CS501", "hours": 3},
    "Machine Learning": {"code": "CS502", "hours": 3},
    "Deep Learning": {"code": "CS503", "hours": 3},
    "Data Structures II": {"code": "CS401", "hours": 3},
    "Database Systems": {"code": "CS402", "hours": 3},
    "Operating Systems": {"code": "CS403", "hours": 3},
    "Introduction to Programming II": {"code": "CS301", "hours": 3},
    "Discrete Mathematics": {"code": "CS302", "hours": 3},
    "Computer Architecture": {"code": "CS303", "hours": 3},
    "Foundations of Computer Science": {"code": "CS201", "hours": 3},
    "Web Development Basics": {"code": "CS202", "hours": 3},
    "IT Support Fundamentals": {"code": "CS203", "hours": 3},
}

# Determine the absolute path to the models directory
MODELS_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'models')

# Load the trained model, scaler, and feature columns
try:
    model = joblib.load(os.path.join(MODELS_DIR, "naive_bayes_model.pkl"))
    scaler = joblib.load(os.path.join(MODELS_DIR, "scaler.pkl"))
    feature_columns = joblib.load(os.path.join(MODELS_DIR, "feature_columns.pkl"))
except FileNotFoundError:
    # This is a fallback for environments where the model might not be trained yet.
    model = None
    scaler = None
    feature_columns = None
    print("Warning: Model files not found. Recommendation engine will use fallback logic.")

def get_recommendations(
    age: int,
    gender: int,
    ethnicity: int,
    parental_education: int,
    study_time_weekly: float,
    absences: int,
    tutoring: int,
    parental_support: int,
    extracurricular: int,
    sports: int,
    music: int,
    volunteering: int,
    gpa: float,
):
    """
    Recommends courses based on student data using a trained model.
    """
    if model is None or scaler is None or feature_columns is None:
        # Fallback logic if the model is not loaded
        st_course = ["Advanced Algorithms", "Machine Learning", "Deep Learning"]
        nd_courses = ["Data Structures II", "Database Systems", "Operating Systems"]
        rd_courses = ["Introduction to Programming II", "Discrete Mathematics", "Computer Architecture"]
        if gpa >= 3.5:
            recommended_courses = random.sample(st_course, k=len(st_course))
            grade_class = "A"
        elif gpa >= 2.5:
            recommended_courses = random.sample(nd_courses, k=len(nd_courses))
            grade_class = "B"
        else:
            recommended_courses = random.sample(rd_courses, k=len(rd_courses))
            grade_class = "C"
        
        courses_with_details = [{"Course Name": name, "Code": COURSE_CATALOG[name]["code"], "Hours": COURSE_CATALOG[name]["hours"]} for name in recommended_courses]
        return grade_class, courses_with_details

    # Create a DataFrame from the input data with columns in the correct order
    input_data = pd.DataFrame(
        [
            {
                "Age": age,
                "Gender": gender,
                "Ethnicity": ethnicity,
                "ParentalEducation": parental_education,
                "StudyTimeWeekly": study_time_weekly,
                "Absences": absences,
                "Tutoring": tutoring,
                "ParentalSupport": parental_support,
                "Extracurricular": extracurricular,
                "Sports": sports,
                "Music": music,
                "Volunteering": volunteering,
                "GPA": gpa,
            }
        ]
    )
    
    # Ensure the order of columns matches the training data
    input_data = input_data[feature_columns]

    # Scale the input data
    input_scaled = scaler.transform(input_data)

    # Predict the GradeClass
    prediction = model.predict(input_scaled)
    grade_class_index = prediction[0]
    grade_class_map = {0: "A", 1: "B", 2: "C", 3: "D"}
    grade_class = grade_class_map.get(grade_class_index, "N/A")

    # Define course recommendations for each grade class
    recommendations_map = {
        0: ["Advanced Algorithms", "Machine Learning", "Deep Learning"],
        1: ["Data Structures II", "Database Systems", "Operating Systems"],
        2: ["Introduction to Programming II", "Discrete Mathematics", "Computer Architecture"],
        3: ["Foundations of Computer Science", "Web Development Basics", "IT Support Fundamentals"],
    }

    # Get recommendations and shuffle them
    recommended_courses = recommendations_map.get(grade_class_index, ["No specific recommendations available."])
    random.shuffle(recommended_courses)
    
    courses_with_details = [{"Name": name, "Code": COURSE_CATALOG.get(name, {}).get("code", "N/A"), "Hours": COURSE_CATALOG.get(name, {}).get("hours", "N/A")} for name in recommended_courses]
    
    return grade_class, courses_with_details
