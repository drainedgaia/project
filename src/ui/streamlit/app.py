import streamlit as st

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
