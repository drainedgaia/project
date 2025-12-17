import streamlit as st
import sys
import os

# Add the project root to the Python path to allow for absolute imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.data.database import init_db, SessionLocal
from src.logic.auth import authenticate_user, create_user
from src.data.models import User

# Initialize the database
init_db()

st.set_page_config(
    page_title="Student Recommendation System",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="expanded",
)

def show_login_page():
    """
    Displays the login and signup page.
    """
    # Hide sidebar
    st.markdown("""
        <style>
            [data-testid="stSidebar"] {
                display: none;
            }
        </style>
    """, unsafe_allow_html=True)

    st.title("Login or Signup")

    login_tab, signup_tab = st.tabs(["Login", "Signup"])

    with login_tab:
        with st.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login")

            if submitted:
                if not email or not password:
                    st.toast("Please fill in all fields.", icon="⚠️")
                else:
                    db = SessionLocal()
                    user = authenticate_user(db, email, password)
                    db.close()
                    if user:
                        st.session_state.authenticated = True
                        st.session_state.user = user
                        st.toast("Login successful!", icon="✅")
                        st.rerun()
                    else:
                        st.toast("Invalid email or password.", icon="❌")

    with signup_tab:
        with st.form("signup_form"):
            first_name = st.text_input("First Name")
            last_name = st.text_input("Last Name")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Signup")

            if submitted:
                if not all([first_name, last_name, email, password]):
                    st.toast("Please fill in all fields.", icon="⚠️")
                else:
                    db = SessionLocal()
                    user_exists = db.query(User).filter(User.email == email).first()
                    if user_exists:
                        st.toast("User with this email already exists.", icon="❌")
                        db.close()
                    else:
                        create_user(db, first_name, last_name, email, password)
                        db.close()
                        st.toast("Signup successful! You can now log in.", icon="✅")

def show_dashboard_page():
    """
    Displays the main dashboard for logged-in users.
    """
    st.title("🎓 Student Recommendation System")
    st.sidebar.success(f"Logged in as {st.session_state.user.first_name}")
    st.markdown("Welcome back! Navigate to the Recommender page to get started.")


def main():
    """
    Main function to route to the correct page.
    """
    # Initialize session state variables
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.session_state.user = None
        st.session_state.recommendations = None

    if st.session_state.authenticated:
        show_dashboard_page()
    else:
        show_login_page()

if __name__ == "__main__":
    main()