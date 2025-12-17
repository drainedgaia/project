import streamlit as st
import pandas as pd
from src.logic.recommender import get_recommendations
from src.utils.validation import validate_gpa

def show_recommender_page():
    """
    Displays the recommender form for logged-in users.
    """
    st.title("Recommender Form")
    st.markdown("Fill in your academic and personal information to get recommendations.")

    with st.form("recommender_form"):
        st.markdown("### Academic and Personal Information")
        
        cols1 = st.columns(3)
        with cols1[0]:
            gpa_input = st.number_input("Previous GPA (0.0-4.0)", min_value=0.0, max_value=4.0, value=3.0, step=0.1)
        with cols1[1]:
            age_input = st.number_input("Age", min_value=10, max_value=100, value=16)
        with cols1[2]:
            study_time_weekly_input = st.slider("Study Time Weekly (hours)", 0, 20, 10)

        absences_input = st.slider("Absences (days)", 0, 30, 5)
        
        cols2 = st.columns(2)
        with cols2[0]:
            education_options = {0: "None", 1: "High School", 2: "Some College", 3: "Bachelor's", 4: "Higher"}
            parental_education_input = st.radio(
                "Parental Education",
                options=education_options.keys(),
                format_func=lambda x: education_options[x],
                index=2
            )
        with cols2[1]:
            support_options = {0: "None", 1: "Low", 2: "Moderate", 3: "High", 4: "Very High"}
            parental_support_input = st.radio(
                "Parental Support",
                options=support_options.keys(),
                format_func=lambda x: support_options[x],
                index=2
            )

        cols3 = st.columns(3)
        with cols3[0]:
            gender_options = {0: "Female", 1: "Male"}
            gender_input = st.radio(
                "Gender",
                options=gender_options.keys(),
                format_func=lambda x: gender_options[x],
                index=0
            )
        with cols3[1]:
            ethnicity_options = {0: "Caucasian", 1: "African American", 2: "Asian", 3: "Other"}
            ethnicity_input = st.radio(
                "Ethnicity",
                options=ethnicity_options.keys(),
                format_func=lambda x: ethnicity_options[x],
                index=0
            )
        with cols3[2]:
            tutoring_options = {0: "No", 1: "Yes"}
            tutoring_input = st.radio(
                "Tutoring",
                options=tutoring_options.keys(),
                format_func=lambda x: tutoring_options[x],
                index=0
            )

        st.markdown("### Activities")
        cols4 = st.columns(4)
        with cols4[0]:
            extracurricular_input = st.checkbox("Extracurricular", value=False)
        with cols4[1]:
            sports_input = st.checkbox("Sports", value=False)
        with cols4[2]:
            music_input = st.checkbox("Music", value=False)
        with cols4[3]:
            volunteering_input = st.checkbox("Volunteering", value=False)

        submitted = st.form_submit_button("Get Recommendations")

        if submitted:
            if not validate_gpa(gpa_input):
                st.toast("Invalid GPA. Please enter a value between 0.0 and 4.0.", icon="⚠️")
            else:
                grade_class, recommended_courses = get_recommendations(
                    age=age_input,
                    gender=gender_input,
                    ethnicity=ethnicity_input,
                    parental_education=parental_education_input,
                    study_time_weekly=study_time_weekly_input,
                    absences=absences_input,
                    tutoring=tutoring_input,
                    parental_support=parental_support_input,
                    extracurricular=int(extracurricular_input),
                    sports=int(sports_input),
                    music=int(music_input),
                    volunteering=int(volunteering_input),
                    gpa=gpa_input,
                )
                
                st.session_state.recommendations = {
                    "grade_class": grade_class,
                    "recommended_courses": recommended_courses,
                    "submitted_data": {
                        "GPA": gpa_input,
                        "Age": age_input,
                        "Study Time Weekly": study_time_weekly_input,
                        "Absences": absences_input
                    }
                }
                st.toast("Recommendations generated successfully!", icon="✅")
                st.switch_page("pages/3_Results.py")


if "authenticated" in st.session_state and st.session_state.authenticated:
    show_recommender_page()
else:
    st.warning("You must be logged in to access the recommender.")
    st.page_link("app.py", label="Go to Login")
    st.stop()
