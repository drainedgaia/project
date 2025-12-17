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
    Displays the login and signup page with improved aesthetics.
    """
    st.markdown("""
        <style>
            [data-testid="stSidebar"] {
                display: none;
            }
            /* Hide the Streamlit footer text */
            [data-testid="stSidebar"] > div:last-child {
                visibility: hidden;
                height: 0%;
                position: fixed;
            }
            /* Optional: Adjust the main content margin if needed */
            [data-testid="stAppViewBlockContainer"] {
                padding-top: 1rem;
            }
        </style>
    """, unsafe_allow_html=True)

    _, col2, _ = st.columns([1, 2, 1])

    with col2:
        st.title("🎓 Student Recommendation System")
        st.markdown("Log in or create an account to receive personalized recommendations.")
        st.write("")

        login_tab, signup_tab = st.tabs(["Login", "Signup"])

        with login_tab:
            with st.form("login_form"):
                email = st.text_input("Email", placeholder="your@email.com")
                password = st.text_input("Password", type="password", placeholder="••••••••")
                st.write("")
                submitted = st.form_submit_button("Login", use_container_width=True, type="primary")

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
                col1, col2 = st.columns(2)
                with col1:
                    first_name = st.text_input("First Name", placeholder="John")
                with col2:
                    last_name = st.text_input("Last Name", placeholder="Doe")
                
                email = st.text_input("Email", placeholder="your@email.com")
                password = st.text_input("Password", type="password", placeholder="••••••••")
                st.write("")
                submitted = st.form_submit_button("Signup", use_container_width=True, type="primary")

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
    Displays the main dashboard for logged-in users with improved aesthetics.
    """
    st.sidebar.success(f"Logged in as {st.session_state.user.first_name}")
    
    st.title("🎓 Dashboard")
    st.markdown(f"### Welcome back, {st.session_state.user.first_name}! 👋")
    st.markdown("You're logged in and ready to explore. Use the options below to get started.")
    st.write("")

    _, col2, _ = st.columns([0.5, 3, 0.5])
    with col2:
        with st.container(border=True):
            st.subheader("📝 Get New Recommendations")
            st.markdown("Fill out the form with your academic and personal information to receive a new set of tailored recommendations.")
            if st.button("Go to Recommender", type="primary", use_container_width=True):
                st.switch_page("pages/2_Recommender.py")

        st.write("")

        with st.container(border=True):
            st.subheader("📊 View Latest Results")
            st.markdown("View the most recent recommendations you have generated. If you haven't generated any yet, this page will be empty.")
            if st.button("Go to Results", use_container_width=True):
                st.switch_page("pages/3_Results.py")


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