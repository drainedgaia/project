import streamlit as st
import sys
import os

# Add the project root to the Python path to allow for absolute imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.data.database import init_db

# Initialize the database
init_db()

st.set_page_config(
    page_title="Student Recommendation System",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="expanded",
)

def main():
    """
    Main function to run the Streamlit application.
    """
    st.title("🎓 Student Recommendation System")

    # Initialize session state variables
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.session_state.user = None
        st.session_state.recommendations = None

    if st.session_state.authenticated:
        st.sidebar.success(f"Logged in as {st.session_state.user.first_name}")
        st.markdown("Welcome back! Navigate to the Recommender page to get started.")
    else:
        st.markdown("Please log in or sign up to continue.")

if __name__ == "__main__":
    main()
