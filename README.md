# Crop Yield Prediction

## Introduction

A Machine Learning-based web application that predicts crop yield using historical crop and weather data. The system integrates ML models, real-time weather data, and user authentication to provide accurate and interactive predictions.


## Features
 * Crop yield prediction using ML models
 * Uses historical crop and weather datasets
 * Real-time weather data via OpenWeather API
 * User authentication (Login & Signup with OTP/email)
 * MySQL database integration
 * Interactive UI built with Streamlit

## Tech Stack
 * **Language**: Python
 * **Libraries**: Pandas, NumPy, Matplotlib, Scikit-learn, XGBoost
 * **Frontend**: Streamlit
 * **Database**: MySQL
 * **API**: OpenWeather API
 * **Authentication**: Email OTP (SMTP)
 * **Security**: Environment variables (.env)

## Installation & Setup
1. **Clone Repository**

```bash
git clone <your-repo-link>
cd Crop-Yield-Prediction
```

2.  **Create Virtual Environment**
```bash
python -m venv venv
```

Activate 
* **Windows**
```bash
venv\Scripts\activate
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

## Environment Variables Setup
This project uses sensitive data:

* Database credentials
* API key
* Email credentials
These are stored in a .env file (NOT included in repo)

1. Create ```bash .env ``` file
```bash
    .env
```
2. Add the following:
 ```bash
# Database
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=Crop_Yield_Prediction

# OpenWeather API
OPENWEATHER_API_KEY=your_api_key

# Email (for OTP)
EMAIL_USER=your_email@gmail.com
EMAIL_PASS=your_app_password
```
3. Install dotenv
```bash
   pip install python-dotenv
```
4. Setup Database
``` bash setup_db.py``` is inside the ``` bash db``` folder, run:
```bash
   python db/setup_db.py
```
This will:

* Create database Crop_Yield_Prediction
* Create users table


## Run the Application
```bash
   streamlit run app.py
```

   




