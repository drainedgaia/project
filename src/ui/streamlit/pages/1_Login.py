import streamlit as st
from src.data.database import SessionLocal
from src.logic.auth import authenticate_user, create_user
from src.data.models import User

def show_login_page():
    """
    Displays the login and signup page.
    """
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

if "authenticated" in st.session_state and not st.session_state.authenticated:
    show_login_page()
else:
    st.markdown("You are already logged in.")
