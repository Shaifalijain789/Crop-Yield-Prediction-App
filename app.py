import streamlit as st
from account import account_page
from prediction import yield_prediction_page
import weather_dashboard 
import crop_dashboard

# ---- Page Configuration ----
st.set_page_config(page_title="Crop Yield Prediction App", layout="wide")

# ============================
# SESSION STATE INITIALIZATION
# ============================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "current_page" not in st.session_state:
    st.session_state.current_page = "Account"
if "auth_mode" not in st.session_state:
    st.session_state.auth_mode = "Signup"

# ============================
# MAIN NAVIGATION
# ============================
# Determine the correct index for the radio button
if st.session_state.logged_in:
    menu_options = ["Account", "Yield Prediction", "Weather Dashboard","Crop Dashboard"]
    if st.session_state.current_page == "Yield Prediction":
        menu_index = 1
    elif st.session_state.current_page == "Weather Dashboard":
        menu_index = 2
    elif st.session_state.current_page == "Crop Dashboard":
        menu_index=3
    else:
        menu_index = 1
else:
    menu_options = ["Account", "Yield Prediction", "Weather Dashboard"," Crop Dashboard"]
    menu_index = 0

menu = st.sidebar.radio("Navigation", menu_options, index=menu_index)

# Prevent going back to Account page when logged in
if st.session_state.logged_in and menu == "Account":
    menu = "Yield Prediction"

# Handle menu selection
if menu == "Account":
    st.session_state.current_page = "Account"

elif menu == "Yield Prediction":
    if st.session_state.get("logged_in", False):
        st.session_state.current_page = "Yield Prediction"
    else:
        st.write("Please login first to access the Yield Prediction page.")
        st.session_state.current_page = "Account"

elif menu == "Weather Dashboard":
    if st.session_state.get("logged_in", False):
        st.session_state.current_page = "Weather Dashboard"
    else:
        st.write("Please login first to access the Weather Dashboard page.")
        st.session_state.current_page = "Account"

else :
    if st.session_state.get("logged_in", False):
        st.session_state.current_page = "Crop Dashboard"
    else:
        st.write("Please login first to access the Crop Dashboard page.")
        st.session_state.current_page = "Account"
        
# Logout button
if st.session_state.logged_in:
        st.sidebar.write("---")
        if st.sidebar.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.current_page = "Account"
            st.rerun() 


# ============================
# PAGE RENDERING
# ============================
if st.session_state.current_page == "Account":
    account_page()
    # if st.session_state.auth_mode == "Login":
    # login_page()  # Your existing login function
elif st.session_state.current_page == "Yield Prediction":
    yield_prediction_page()
elif st.session_state.current_page == "Weather Dashboard":
    weather_dashboard.weather_dashboard()
elif st.session_state.current_page == "Crop Dashboard":
    crop_dashboard.crop_dashboard()
    
    
    
