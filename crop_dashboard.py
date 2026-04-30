import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import base64

# Load dataset
df = pd.read_csv("ml model/Crop_Weather_data.csv")
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

# ---------------- User Inputs ----------------
def crop_dashboard():
  load_css()
  set_background("assets/image/dashboard.jpg")
  st.title("Crop Dashboard")
  state = st.selectbox("Select State", sorted(df["STATE"].unique()))
  crop = st.selectbox("Select Crop", sorted(df["CROP"].unique()))

  col1, col2 = st.columns(2)

  with col1:
    start_year = st.number_input(
        "Enter Start Year",
        min_value=int(df["YEAR"].min()),
        max_value=int(df["YEAR"].max()),
        value=int(df["YEAR"].min())
    )

  with col2:
     end_year = st.number_input(
        "Enter End Year",
        min_value=int(df["YEAR"].min()),
        max_value=int(df["YEAR"].max()),
        value=int(df["YEAR"].max())
    )

# ---------------- Validation ----------------
  if start_year > end_year:
    st.error("Start year must be less than or equal to end year")
    st.stop()

# ---------------- Filter Data ----------------
  filtered_df = df[
    (df["STATE"] == state) &
    (df["CROP"] == crop) &
    (df["YEAR"] >= start_year) &
    (df["YEAR"] <= end_year)
  ]

  if filtered_df.empty:
    st.warning("No data available for selected inputs")
    st.stop()

# ---------------- Aggregate ----------------
  avg_yield_year = (
    filtered_df
    .groupby("YEAR")["YIELD_TON_HA"]
    .mean()
    .reset_index()
  )

# ---------------- Plot ----------------
  st.subheader(f"Average Yield Trend ({crop} in {state})")

  fig, ax = plt.subplots(figsize=(9, 4))
  ax.plot(
    avg_yield_year["YEAR"],
    avg_yield_year["YIELD_TON_HA"],
    marker="o",
    linewidth=2
 )

  ax.set_xlabel("Year")
  ax.set_ylabel("Average Yield (Ton/Ha)")
  st.pyplot(fig)