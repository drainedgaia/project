import streamlit as st
import pandas as pd

def show_results_page():
    """
    Displays the recommendation results to the user.
    """
    st.title("Your Recommendations")

    if st.session_state.recommendations:
        user = st.session_state.user
        recs = st.session_state.recommendations
        
        st.markdown("### Summary of Your Information")
        
        info_cols = st.columns(2)
        with info_cols[0]:
            st.markdown(f"**Name:** {user.first_name} {user.last_name}")
            st.markdown(f"**Email:** {user.email}")
        with info_cols[1]:
            for key, value in recs["submitted_data"].items():
                st.markdown(f"**{key}:** {value}")

        st.markdown("---")
        
        st.markdown(f"### Estimated Grade: **{recs['grade_class']}**")

        st.markdown("### Recommended Courses")
        recommendations_df = pd.DataFrame(recs["recommended_courses"])
        st.dataframe(recommendations_df)

    else:
        st.warning("No recommendations found. Please fill out the recommender form first.")
        st.page_link("pages/2_Recommender.py", label="Go to Recommender")


if "authenticated" in st.session_state and st.session_state.authenticated:
    show_results_page()
else:
    st.warning("You must be logged in to view results.")
    st.page_link("pages/1_Login.py", label="Go to Login")
