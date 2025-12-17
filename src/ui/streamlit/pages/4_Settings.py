import streamlit as st
from src.data.database import SessionLocal
from src.data.models import User
import time

def show_settings_page():
    """
    Displays the settings page for logged-in users.
    """
    st.title("⚙️ Settings")

    # --- User Profile Section ---
    st.header("User Profile")
    user = st.session_state.user
    
    with st.form("profile_form"):
        st.write(f"**Email:** {user.email}")  # Email is not editable
        
        col1, col2 = st.columns(2)
        with col1:
            first_name = st.text_input("First Name", value=user.first_name)
        with col2:
            last_name = st.text_input("Last Name", value=user.last_name)
            
        submitted = st.form_submit_button("Update Profile", use_container_width=True, type="primary")
        if submitted:
            if not first_name or not last_name:
                st.toast("Name fields cannot be empty.", icon="⚠️")
            else:
                db = SessionLocal()
                db_user = db.query(User).filter(User.id == user.id).first()
                if db_user:
                    db_user.first_name = first_name
                    db_user.last_name = last_name
                    db.commit()
                    st.session_state.user = db_user  # Update the user object in session state
                    db.refresh(db_user)
                    db.close()
                    st.toast("Profile updated successfully!", icon="✅")
                    time.sleep(1) # Give toast time to show
                    st.rerun()
                else:
                    db.close()
                    st.toast("Could not find user to update.", icon="❌")

    st.markdown("---")

    # --- Account Actions Section ---
    st.header("Account Actions")

    # Logout Button
    st.write("Log out of your account. You will be returned to the login page.")
    if st.button("Logout", use_container_width=True):
        st.session_state.authenticated = False
        st.session_state.user = None
        st.session_state.recommendations = None
        st.toast("You have been logged out.", icon="👋")
        time.sleep(1)
        st.rerun()

    # Delete Account Button
    st.write("")
    st.subheader("Delete Account")
    st.warning("This action is irreversible. All your data will be permanently deleted.")
    
    with st.expander("Click here to confirm account deletion"):
        st.markdown("Are you absolutely sure you want to delete your account? This cannot be undone.")
        if st.button("Yes, I want to delete my account", type="primary", use_container_width=True):
            db = SessionLocal()
            db_user = db.query(User).filter(User.id == st.session_state.user.id).first()
            if db_user:
                db.delete(db_user)
                db.commit()
                db.close()
                st.session_state.authenticated = False
                st.session_state.user = None
                st.session_state.recommendations = None
                st.toast("Your account has been deleted.", icon="🗑️")
                time.sleep(1)
                st.rerun()
            else:
                db.close()
                st.toast("Could not find user to delete.", icon="❌")


# --- Authentication Check ---
if "authenticated" in st.session_state and st.session_state.authenticated:
    show_settings_page()
else:
    st.warning("You must be logged in to access settings.")
    st.page_link("app.py", label="Go to Login")
    st.stop()
