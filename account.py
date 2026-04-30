import streamlit as st
from login import login_page
from signup_page import signup_page  

def set_account_bg_style():
    """Set background image and style."""
    css = """
    <style>
    .stApp {
        background-image: linear-gradient(rgba(0,0,0,0.4), rgba(0,0,0,0.4)),
                          url("https://www.shutterstock.com/image-photo/lush-rice-paddy-field-neat-600nw-2499404003.jpg");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        background-position: center;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

def account_page():
    """Switch between Login and Signup pages."""
    try:
        with open("assets/style.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("CSS file not found.")

    set_account_bg_style()

    if "auth_mode" not in st.session_state:
        st.session_state.auth_mode = "Login"

    if st.session_state.auth_mode == "Login":
        login_page()
    else:
        signup_page()


