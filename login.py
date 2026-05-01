import streamlit as st
import time
import mysql.connector
from mysql.connector import Error
import bcrypt
from dotenv import load_dotenv
import os
# ==========================
# CENTERED INPUT
# ==========================
def centered_input(label, key, placeholder="", input_type="text"):
    """Create a centered input field."""
    col1, col2, col3 = st.columns([2, 4, 2])
    with col2:
        st.markdown(f"<p class='form-label'>{label}</p>", unsafe_allow_html=True)
        if input_type == "text":
            return st.text_input(label, placeholder=placeholder, key=key, label_visibility="collapsed")
        elif input_type == "password":
            return st.text_input(label, type="password", placeholder=placeholder, key=key, label_visibility="collapsed")

# ==========================
# DB CHECK FUNCTION
# ==========================

load_dotenv()
def check_user_credentials(email, password):
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        cursor = connection.cursor()

        # Fetch stored hash for this email
        cursor.execute("SELECT Password FROM users WHERE Email = %s", (email,))
        result = cursor.fetchone()

        if result is None:
            return False, "No account found with this email."

        stored_hash = result[0]

        # Verify password against stored hash
        if bcrypt.checkpw(password.encode("utf-8"), stored_hash.encode("utf-8")):
            return True, "Login successful!"
        else:
            return False, "Incorrect password."
    except Error as e:
        return False, f"Database error: {e}"
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

# ==========================
# LOGIN PAGE
# ==========================
def login_page():
    """Display the login form."""
    # Load CSS
    with open("assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    
    st.markdown("<h1 class='center-title'>Login to Your Account</h1>", unsafe_allow_html=True)
    
    email = centered_input("Email", "login_email", "Enter your email")
    password = centered_input("Password", "login_password", "Enter your password", input_type="password")
    
    col1, col2, col3 = st.columns([2, 4, 2])
    with col2:
        if st.button("Login", key="login_button"):
            if email and password:
                success, msg = check_user_credentials(email, password)
                if success:
                    st.markdown(f"<p style='color:white; '>{msg}</p>", unsafe_allow_html=True)
                    st.session_state.logged_in = True
                    st.session_state.current_page = "Yield Prediction"
                    # st.success(msg)
                    time.sleep(1)
                    st.rerun()
                else:
                    st.markdown(f"<p style='color:white; '>{msg}</p>", unsafe_allow_html=True)
                    # st.error(msg)
            else:
                st.markdown("Please enter both email and password")
    
    col1, col2, col3 = st.columns([3, 2, 3])
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Don't have an account? Sign Up", key="switch_to_signup"):
            st.session_state.auth_mode = "Signup"
            st.rerun()

# Run directly
if __name__ == "__main__":
    login_page()
