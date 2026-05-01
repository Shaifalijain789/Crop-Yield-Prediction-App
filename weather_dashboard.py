import streamlit as st
import requests
from datetime import datetime
import base64
from dotenv import load_dotenv
import os

# ---------------- CONFIG ----------------

load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

GEOCODE_URL = "https://api.openweathermap.org/geo/1.0/direct"
CURRENT_WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
ONECALL_URL = "https://api.openweathermap.org/data/3.0/onecall"

def set_background(image_file):
    with open(image_file, "rb") as file:
        encoded = base64.b64encode(file.read()).decode()

    st.markdown(
        f"""
        <style>
        [data-testid="stAppViewContainer"] {{
            background-image: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        [data-testid="stHeader"], [data-testid="stSidebar"] {{
            background: rgba(255, 255, 255, 0.4);
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


def load_css():
    with open("assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ---------------- API FUNCTIONS ----------------
def get_coordinates(location):
    try:
        params = {
            "q": f"{location},IN",
            "limit": 1,
            "appid": API_KEY
        }

        response = requests.get(GEOCODE_URL, params=params, timeout=5)

        if response.status_code != 200:
            return "api_error"

        data = response.json()

        if not data:
            return None

        return {
            "lat": data[0]["lat"],
            "lon": data[0]["lon"],
            "city": data[0]["name"],
            "state": data[0].get("state", "")
        }

    except requests.exceptions.ConnectionError:
        return "no_internet"

    except requests.exceptions.Timeout:
        return "timeout"

    except requests.exceptions.RequestException:
        return "api_error"
    

def get_current_weather(lat, lon):
    try:
        params = {
            "lat": lat,
            "lon": lon,
            "appid": API_KEY,
            "units": "metric"
        }

        response = requests.get(CURRENT_WEATHER_URL, params=params, timeout=5)
        return response.json()

    except requests.exceptions.ConnectionError:
        return "no_internet"

    except requests.exceptions.RequestException:
        return None


def get_rain_probability(lat, lon):
    params = {
        "lat": lat,
        "lon": lon,
        "appid": API_KEY,
        "units": "metric",
        "exclude": "minutely,daily,alerts"
    }
    response = requests.get(ONECALL_URL, params=params)
    data = response.json()

    if "hourly" in data and data["hourly"]:
        return int(data["hourly"][0].get("pop", 0) * 100)
    return 0


def safe_request(url, params):
    try:
        return requests.get(url, params=params, timeout=5)
    except requests.exceptions.ConnectionError:
        return "no_internet"


# ---------------- DASHBOARD FUNCTION ----------------
def weather_dashboard():
     
    load_css()
    set_background("assets/image/dashboard.jpg")
    st.title("Real-Time Weather Dashboard (India)")
    

    location = st.text_input(
        "Enter your district name",
        placeholder="Example: Jhansi / Rampur UP"
    )

    if st.button("Get Weather"):
        if not location.strip():
            st.warning("Please enter the district name")
            return

        # with st.spinner("Fetching weather data..."):
        geo_data = get_coordinates(location)

        if geo_data == "no_internet":
            st.error("Check your internet connection and try again.")
            return

        elif geo_data == "timeout":
            st.error("Request timed out. Please try again.")
            return

        elif geo_data == "api_error":
            st.error("Server error. Please try later.")
            return

        elif geo_data is None:
            st.error("Location not found. Try including district or state.")
            return

        weather = get_current_weather(geo_data["lat"], geo_data["lon"])

        if weather == "no_internet":
            st.error("Check your internet connection.")
            return

        if weather is None or "main" not in weather:
            st.error("Unable to fetch weather data.")
            return
        rain_prob = get_rain_probability(geo_data["lat"], geo_data["lon"])

        
        st.subheader(f"{geo_data['city']}, {geo_data['state']}, India")

        c1, c2 = st.columns(2)
        c1.metric("Temperature", f"{weather['main']['temp']} °C")
        c2.metric("Humidity", f"{weather['main']['humidity']} %")
           
            
        c1.metric("Wind Speed", f"{weather['wind']['speed']} m/s")
        c2.metric("Chance of Rain",f"{rain_prob} %")

        sunrise = datetime.fromtimestamp(weather["sys"]["sunrise"])
        sunset = datetime.fromtimestamp(weather["sys"]["sunset"])

        st.markdown("---")
        
        st.write(f"Sunrise: {sunrise.strftime('%I:%M %p')}")
        st.write(f"Sunset: {sunset.strftime('%I:%M %p')}")

        st.markdown(
                f" Last updated: {datetime.now().strftime('%d %b %Y, %I:%M %p')}"
            )


