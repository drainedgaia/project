import joblib
import pandas as pd
import numpy as np
import os
import random

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
            return random.sample(st_course, k=len(st_course))
        elif gpa >= 2.5:
            return random.sample(nd_courses, k=len(nd_courses))
        else:
            return random.sample(rd_courses, k=len(rd_courses))

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
    grade_class = prediction[0]

    # Define course recommendations for each grade class
    recommendations_map = {
        0: ["Advanced Algorithms", "Machine Learning", "Deep Learning"],
        1: ["Data Structures II", "Database Systems", "Operating Systems"],
        2: ["Introduction to Programming II", "Discrete Mathematics", "Computer Architecture"],
        3: ["Foundations of Computer Science", "Web Development Basics", "IT Support Fundamentals"],
    }

    # Get recommendations and shuffle them
    recommended_courses = recommendations_map.get(grade_class, ["No specific recommendations available."])
    random.shuffle(recommended_courses)
    
    return recommended_courses