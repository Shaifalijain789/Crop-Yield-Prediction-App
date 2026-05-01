import streamlit as st
import time
import smtplib
import random
import re
import mysql.connector
from mysql.connector import Error
import bcrypt
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os


# ==========================
# OTP GENERATION & EMAIL
# ==========================

load_dotenv()

def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp_email(receiver_email, otp):
    sender_email = os.getenv("EMAIL_USER")
    sender_password = os.getenv("EMAIL_PASS") # Gmail app password

    subject = "Your OTP Verification Code"
    body = f"Your OTP is: {otp}\nDo not share it with anyone."

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587, timeout=15) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
        st.session_state.email_error = ""
        return True
    except Exception as e:
        st.session_state.email_error = str(e)
        return False

# ==========================
# EMAIL VALIDATION
# ==========================
def is_valid_email(email: str) -> bool:
    pattern = r"^[\w\.\-+]+@[\w\-]+\.[\w\.\-]+$"
    return bool(re.match(pattern, email))

# ==========================
# DB INSERT FUNCTION
# ==========================
def save_user_to_db(username, email, password):
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        cursor = connection.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM users WHERE Email = %s", (email,))
        (count,) = cursor.fetchone()
        if count > 0:
            return False, "User with this email is already registered."

        # hash password and decode to string
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")

        insert_query = """
        INSERT INTO users (username, email, password)
        VALUES (%s, %s, %s)
        """
        cursor.execute(insert_query, (username, email, hashed_password))
        connection.commit()
        return True, "User register successfully!"
    except Error as e:
        return False, f"Database error: {e}"
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

# ==========================
# CENTERED INPUT
# ==========================
def centered_input(label, key, placeholder="", input_type="text"):
    col1, col2, col3 = st.columns([2, 4, 2])
    with col2:
        st.markdown(f"<p class='form-label'>{label}</p>", unsafe_allow_html=True)
        if input_type == "password":
            return st.text_input(label, placeholder=placeholder, key=key,
                                 label_visibility="collapsed", type="password")
        return st.text_input(label, placeholder=placeholder, key=key,
                             label_visibility="collapsed")

# ==========================
# SIGNUP PAGE
# ==========================
def signup_page():
    st.markdown("<h1 class='center-title'>Create Your Account</h1>", unsafe_allow_html=True)

    username = centered_input("Username", "signup_username", "Enter username")
    email = centered_input("Email", "signup_email", "Enter your email")
    password = centered_input("Password", "signup_password", "Enter password", input_type="password")
    confirm_password = centered_input("Confirm Password", "signup_confirm_password",
                                      "Re-enter password", input_type="password")
    otp = centered_input("OTP", "signup_otp", "Enter OTP sent to email")

    # Initialize session variables
    for key in ["otp_start_time", "otp_running", "generated_otp", "show_resend", "email_error"]:
        if key not in st.session_state:
            st.session_state[key] = None if key != "show_resend" else False

    col1, col2, col3 = st.columns([2, 4, 2])
    with col2:
        left_col, right_col = st.columns([4, 1.5])
        countdown_placeholder = st.empty()

        # ===================== GENERATE / RESEND OTP =====================
        with left_col:
            otp_button = st.button("Resend OTP") if st.session_state.show_resend else st.button("Generate OTP")
            if otp_button:
                if not password or not confirm_password:
                    st.markdown("Please enter password and confirm password before requesting OTP.")
                elif password != confirm_password:
                    st.markdown("Passwords do not match! Fix them before generating OTP.")
                elif not email:
                    st.markdown("Please enter your email first!")
                elif not is_valid_email(email):
                    
                    st.markdown("Please enter a valid email address (looks like user@domain.com).")
                else:
                    otp_value = generate_otp()
                    st.session_state.generated_otp = otp_value
                    st.session_state.otp_start_time = time.time()
                    st.session_state.otp_running = True
                    st.session_state.show_resend = False

                    sent = send_otp_email(email, otp_value)
                    if sent:
                        st.markdown(f"OTP sent successfully to {email}")
                        for remaining in range(30, 0, -1):
                            countdown_placeholder.markdown(f"Resend OTP in {remaining} seconds...")
                            time.sleep(1)
                        st.session_state.otp_running = False
                        st.session_state.show_resend = True
                        st.rerun()
                    else:
                        st.markdown(f"Failed to send OTP: {st.session_state.get('email_error', '')}")

        # ===================== CREATE ACCOUNT =====================
        with right_col:
            if st.button("Create My Account"):
                if not (username and email and password and confirm_password and otp):
                    st.markdown("Please fill all fields including OTP.")
                elif password != confirm_password:
                    st.markdown("Passwords do not match!")
                elif st.session_state.get("generated_otp") != otp:
                    st.markdown("Incorrect OTP! Please enter the correct OTP.")
                else:
                    success, msg = save_user_to_db(username, email, password)
                    if success:
                      st.markdown(f"<p style='color:white; '>{msg}</p>", unsafe_allow_html=True)
                      st.session_state.logged_in = True
                      st.session_state.current_page = "Yield Prediction"
                      time.sleep(1)
                      st.rerun()
                    else:
                      st.markdown(f"<p style='color:white;'>{msg}</p>", unsafe_allow_html=True)

    # ===================== SWITCH TO LOGIN =====================
    col1, col2, col3 = st.columns([4, 1.5, 4])
    with col2:
        if st.button("Already have an account? Login"):
            st.session_state.auth_mode = "Login"
            st.rerun()
# Run directly
if __name__ == "__main__":
    signup_page()
