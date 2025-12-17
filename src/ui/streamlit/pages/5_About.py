import streamlit as st

st.set_page_config(
    page_title="About",
    page_icon="ℹ️",
)

st.title("ℹ️ About the Student Recommendation System")

st.markdown("""
This application is a proof-of-concept student recommendation system designed to help students and educators. 
By inputting academic and personal data, the system provides an estimated grade classification and suggests relevant courses.
""")

st.header("Purpose")
st.markdown("""
Our goal is to provide a tool that can:
-   **Guide Students:** Help students understand their academic standing and discover courses that align with their profile.
-   **Assist Educators:** Offer educators insights into student performance and help them provide targeted support.
-   **Promote Data-Driven Decisions:** Encourage the use of data to make informed decisions about education pathways.
""")

st.header("Technology")
st.markdown("""
This interactive web application is built using a modern Python stack, including:
-   **Streamlit:** For the user interface and interactive components.
-   **Pandas & Scikit-learn:** For data manipulation and the underlying recommendation model.
-   **SQLAlchemy:** For database interactions.
""")

st.markdown("---")

st.header("Contact Us")
st.markdown("""
Have questions, feedback, or suggestions? We'd love to hear from you!

-   **Email:** drainedgaia@gmail.com
-   **GitHub:** [github.com/drainedgaia](https://github.com/drainedgaia/project)
""")
