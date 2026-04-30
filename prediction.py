import streamlit as st
import pandas as pd
import joblib


@st.cache_resource
def load_model():
    return joblib.load("ml model/model.pkl")

model = load_model()

@st.cache_resource
def load_metrics():
    return joblib.load("ml model/model_metrics.pkl")

metrics= load_metrics()

# -------------------------------
# Background Style
# -------------------------------
def set_yield_prediction_style():
    css = """
    <style>
    .stApp {
        background-image: linear-gradient(rgba(0,0,0,0.3), rgba(0,0,0,0.3)),
                          url("https://images.unsplash.com/photo-1625246333195-78d9c38ad449");
        background-size: cover;
        background-attachment: fixed;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


def yield_prediction_page():
    #Load CSS from assets folder
    with open("assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    
    # Set background
    set_yield_prediction_style()
    
    st.markdown(
        "<h1 style='text-align:center; color:white;'>Crop Yield Prediction </h1>",
        unsafe_allow_html=True
    )

    # -------------------------------
    # Inputs
    # -------------------------------
    col1, col2 = st.columns(2)

    with col1:
        state = st.selectbox(
            "State",
            ["Choose", "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar",
             "Chandigarh", "Chhattisgarh",  "Delhi",
             "Goa", "Gujarat", "Haryana", "Himachal Pradesh",
             "Jharkhand", "karnataka", "Kerla", "Ladakh", "Maharashtra",
             "Manipur", "Meghalaya", "Mizoram", "Madhya Pradesh", "Nagaland", "Odisha",
             "Puducherry", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu",
             "Telangana", "Tripura", "Uttarakhand", "Uttar Pradesh",
             "West Bengal"]
        )
        season = st.selectbox(
            "Season",
            ["Choose", "Kharif", "Rabi", "Summer",  "Autumn"]
        )

        avg_temp = st.number_input(
            "Average Temperature (°C)",
            min_value=0.0,
            max_value=60.0,
            value=30.0
        )

    with col2:
        crop = st.text_input("Crop Name", placeholder="Rice / Wheat / Maize")

        rainfall = st.number_input(
            "Rainfall (mm)",
            min_value=0.0,
            value=200.0
        )

        area = st.number_input(
            "Area (Hectares)",
            min_value=0.1,
            value=1.0
        )

    col1, col2, col3 = st.columns([8, 2, 8])

    with col2:
        predict_clicked = st.button("Predict Yield", use_container_width=True)

    if predict_clicked:

        if (
            season != "Choose"
            and state != "Choose"
            and crop.strip() != ""
            and area > 0
        ):
            input_df = pd.DataFrame([{
                "STATE": state,
                "CROP": crop,
                "SEASON": season,
                "AREA_HECTARE": area,
                "T2M": avg_temp,
                "PRECTOTCORR": rainfall
            }])

            prediction = model.predict(input_df)[0]
            total_yield = prediction * area

            # st.success("Prediction Successful")
            st.markdown(f"#### Yield per Hectare: **{prediction:.2f} Ton/Ha**")
            st.markdown(f"#### Total Estimated Yield: **{total_yield:.2f} Tonnes**")

        else:
            st.markdown("Please fill all required fields correctly.")
            
        col1, col2, col3 = st.columns(3)
        m = metrics[0]

        st.markdown("### Model Performance")
        
        st.markdown(f"#### R²: {m['R2']:.2f}")
        st.markdown(f"#### MAE: {m['MAE']:.2f}")
        st.markdown(f"#### RMSE: {m['RMSE']:.2f}")
        
        
        
        # col1, col2, col3 = st.columns(3)

        # col1.metric("R² ", f"{m['R2']:.2f}")
        # col2.metric("MAE ", f"{m['MAE']:.2f}")
        # col3.metric("RMSE ", f"{m['RMSE']:.2f}")



    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

