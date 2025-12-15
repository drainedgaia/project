import gradio as gr
from src.data.database import init_db, SessionLocal
from src.ui.login_page import show_login_page
from src.ui.gradio_app import app as recommender_app
from src.logic.auth import authenticate_user

def main():
    init_db()
    
    login_app = show_login_page()
    
    with gr.Blocks() as app:
        user_state = gr.State(None)
        
        with gr.Column(visible=True) as login_view:
            with gr.Tabs():
                with gr.TabItem("Login"):
                    email_input = gr.Textbox(label="Email")
                    password_input = gr.Textbox(label="Password", type="password")
                    login_button = gr.Button("Login")
                with gr.TabItem("Signup"):
                    signup_first_name = gr.Textbox(label="First Name")
                    signup_last_name = gr.Textbox(label="Last Name")
                    signup_email = gr.Textbox(label="Email")
                    signup_password = gr.Textbox(label="Password", type="password")
                    signup_button = gr.Button("Signup")

        with gr.Column(visible=False) as main_app_view:
            recommender_app_ui = recommender_app(user_state)
        
        def login(email, password):
            if not email or not password:
                gr.Warning("Please fill in all fields.")
                return None, gr.update(visible=True), gr.update(visible=False)
            
            db = SessionLocal()
            user = authenticate_user(db, email, password)
            db.close()

            if user:
                gr.Info("Login successful!")
                return user, gr.update(visible=False), gr.update(visible=True)
            else:
                gr.Warning("Invalid email or password.")
                return None, gr.update(visible=True), gr.update(visible=False)

        def signup(first_name, last_name, email, password):
            # This is a simplified signup, ideally it should be in a separate function
            from src.logic.auth import create_user
            from src.data.database import User
            if not all([first_name, last_name, email, password]):
                gr.Warning("Please fill in all fields.")
                return
            
            db = SessionLocal()
            user = db.query(User).filter(User.email == email).first()
            if user:
                gr.Warning("User with this email already exists.")
                db.close()
                return
            
            create_user(db, first_name, last_name, email, password)
            db.close()
            gr.Info("Signup successful! You can now login.")


        login_button.click(login, inputs=[email_input, password_input], outputs=[user_state, login_view, main_app_view])
        signup_button.click(signup, inputs=[signup_first_name, signup_last_name, signup_email, signup_password], outputs=[])

    app.launch(share=True)

if __name__ == "__main__":
    main()