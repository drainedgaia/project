
import gradio as gr
from sqlalchemy.orm import Session
from src.data.database import SessionLocal
from src.logic.auth import create_user, authenticate_user
from src.utils.validation import validate_email

def signup_page():
    with gr.Blocks() as signup_app:
        gr.Markdown("# Signup")
        first_name_input = gr.Textbox(label="First Name")
        last_name_input = gr.Textbox(label="Last Name")
        email_input = gr.Textbox(label="Email")
        password_input = gr.Textbox(label="Password", type="password")
        signup_button = gr.Button("Signup")
        
        @signup_button.click(inputs=[first_name_input, last_name_input, email_input, password_input], outputs=[])
        def signup(first_name, last_name, email, password):
            if not all([first_name, last_name, email, password]):
                gr.Warning("Please fill in all fields.")
                return
            if not validate_email(email):
                gr.Warning("Invalid email format.")
                return
            
            db: Session = SessionLocal()
            user = db.query(User).filter(User.email == email).first()
            if user:
                gr.Warning("User with this email already exists.")
                db.close()
                return
            
            create_user(db, first_name, last_name, email, password)
            db.close()
            gr.Info("Signup successful! You can now login.")
            return gr.update(visible=False)

    return signup_app

def login_page():
    with gr.Blocks() as login_app:
        gr.Markdown("# Login")
        email_input = gr.Textbox(label="Email")
        password_input = gr.Textbox(label="Password", type="password")
        login_button = gr.Button("Login")

        @login_button.click(inputs=[email_input, password_input], outputs=[])
        def login(email, password):
            if not email or not password:
                gr.Warning("Please fill in all fields.")
                return
            
            db: Session = SessionLocal()
            user = authenticate_user(db, email, password)
            db.close()

            if user:
                gr.Info("Login successful!")
                return user
            else:
                gr.Warning("Invalid email or password.")
                return None
    
    return login_app

def show_login_page():
    with gr.Blocks() as app:
        with gr.Tabs():
            with gr.TabItem("Login"):
                login_page()
            with gr.TabItem("Signup"):
                signup_page()
    return app
