import streamlit as st
import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Get API key (local: from .env, cloud: from secrets)
API_KEY = os.getenv("WEATHERAPI_KEY") or st.secrets.get("WEATHERAPI_KEY")

# Set page configuration
st.set_page_config(
    page_title="Weather App 🌤️",
    page_icon="🌤️",
    layout="wide"
)

# Sidebar for app title and input
with st.sidebar:
    st.title("🌤️ Weather App")
 
    city = st.text_input("Enter the city name:")

if not API_KEY:
    st.sidebar.error("API Key not found. Please set it in .env for local or as a secret for deployment.")
else:
    # Main app layout
    st.markdown(
        """
        <style>
        body {
            background-color: #f8f9fa; /* Light gray background */
        }
        .block-container {
            padding: 2rem;
        }
        .weather-container {
            background-color: #ffffff; /* White card background */
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
        }
        h1, h2, h3, h4, h5, h6 {
            color: #333333; /* Dark gray titles */
        }
        p {
            color: #555555; /* Medium gray for text */
        }
        .sidebar .sidebar-content {
            background-color: #f1f3f5; /* Sidebar light gray */
        }
        .stSidebar {
            background-color: #f1f3f5; /* Adjust for older Streamlit versions */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.title("🌤️ Welcome to WeatherVista")
    st.subheader("Stay updated with real-time weather updates for cities worldwide.")

    if city:
        # WeatherAPI endpoint
        BASE_URL = "http://api.weatherapi.com/v1/current.json"

        # Make API request
        params = {"key": API_KEY, "q": city, "aqi": "no"}
        response = requests.get(BASE_URL, params=params)

        if response.status_code == 200:
            data = response.json()

            # Extract weather data
            location = data["location"]["name"]
            region = data["location"]["region"]
            country = data["location"]["country"]
            temp_c = data["current"]["temp_c"]
            condition = data["current"]["condition"]["text"]
            wind_kph = data["current"]["wind_kph"]
            humidity = data["current"]["humidity"]
            icon = data["current"]["condition"]["icon"]

            # Weather display container
            with st.container():
                st.markdown(
                    f"""
                    <div class="weather-container">
                        <h2>Weather in {location}, {region}, {country}</h2>
                        <div style="display: flex; align-items: center;">
                            <img src="https:{icon}" alt="Weather Icon" style="width: 80px; height: 80px; margin-right: 20px;">
                            <div>
                                <p><strong>Condition:</strong> {condition}</p>
                                <p><strong>Temperature:</strong> {temp_c}°C</p>
                                <p><strong>Wind Speed:</strong> {wind_kph} km/h</p>
                                <p><strong>Humidity:</strong> {humidity}%</p>
                            </div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        else:
            st.error("City not found. Please try again.")
