import streamlit as st
import os
import requests
import os
from kerykeion import AstrologicalSubject, KerykeionChartSVG
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import psycopg2
from datetime import datetime
from io import BytesIO
import base64

<<<<<<< HEAD
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

def get_location(city, country):
    """Fetch latitude, longitude, and timezone for a given city and country."""
    geolocator = Nominatim(user_agent="horacle-astrology-app")  # ✅ Custom user agent
    location_query = f"{city}, {country}"

    try:
        location = geolocator.geocode(location_query, timeout=10)
        if location:
            lat = location.latitude
            lon = location.longitude
            print(f"✅ Found location: {location_query} -> {lat}, {lon}")
            return lat, lon, "UTC"  # ⏳ Default timezone (we can improve this)
        else:
            print(f"❌ Location not found: {location_query}")
            return None, None, None
    except GeocoderTimedOut:
        print("❌ Geopy request timed out. Try again.")
        return None, None, None

# API URLs
DEEPSEEK_URL = "https://api.deepseek.com/v1/chat/completions"
KERYKEION_URL = "https://astrologer.p.rapidapi.com/api/v4/now"

# Access secrets safely
deepseek_api_key = st.secrets.get("DEEPSEEK_API_KEY", None)
kerykeion_api_key = st.secrets.get("KERYKEION_API_KEY", None)
database_url = st.secrets.get("DATABASE_URL", None)

if not all([deepseek_api_key, kerykeion_api_key, database_url]):
    st.error("Missing API keys or database URL in secrets!")
=======
# Debugging: Print the current working directory
st.write("Current Working Directory:", os.getcwd())

# Debugging: Print all secrets
st.write("Secrets:", st.secrets)

# Access the API key
if "DEEPSEEK_API_KEY" in st.secrets:
    deepseek_api_key = st.secrets["DEEPSEEK_API_KEY"]
    st.write("Deepseek API Key:", deepseek_api_key)
else:
    st.error("DEEPSEEK_API_KEY not found in secrets!")

# Access secrets
deepseek_api_key = st.secrets["DEEPSEEK_API_KEY"]
kerykeion_api_key = st.secrets["KERYKEION_API_KEY"]
database_url = st.secrets["DATABASE_URL"]
>>>>>>> 8c724ac4 (updated horaclebot.py with import os and added lines for debugging secret.toml file)

# Initialize session state for user data and token count
if "token_count" not in st.session_state:
    st.session_state.token_count = 5  # Free threshold: 5 tokens

# Function to generate responses using DeepSeek-V3
def generate_response(prompt):
    headers = {
        "Authorization": f"Bearer {deepseek_api_key}",
        "Content-Type": "application/json",
    }
    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "You are an astrology expert."},
            {"role": "user", "content": prompt},
        ],
        "max_tokens": 200,
        "temperature": 0.7,
    }
    try:
        response = requests.post(DEEPSEEK_URL, headers=headers, json=data)
        print("Response Status:", response.status_code)  
        print("Response Text:", response.text)

        response.raise_for_status()
        return response.json().get("choices", [{}])[0].get("message", {}).get("content", "No response available.")
    except requests.exceptions.RequestException as e:
        st.error(f"API request failed: {e}")
        return "Sorry, there was an issue retrieving the response."

# Function to get user's location
def get_user_location():
    try:
        response = requests.get("https://ipinfo.io/json")
        response.raise_for_status()
        location_data = response.json()
        return location_data.get("city", "Unknown"), location_data.get("country", "Unknown")
    except requests.exceptions.RequestException:
        return "Unknown", "Unknown"
            
# Function to fetch current Astrology
def fetch_current_astrology():
    city, country = get_user_location()  # 🌍 Get user's city & country

    url = "https://astrologer.p.rapidapi.com/api/v4/now"

    headers = {
        "x-rapidapi-key": "ca36b5c02fmsh98cdb6706a8ed4cp1a7e21jsnc5522b428380",  
        "x-rapidapi-host": "astrologer.p.rapidapi.com",
        "Accept": "application/json"
    }

    try:
        response = requests.get(url, headers=headers)

        # Debugging
        print("Response Status:", response.status_code)
        print("Response Data:", response.text)

        response.raise_for_status()  # Raise an error for 4xx/5xx responses

        astrology_data = response.json()
        astrology_data["user_city"] = city
        astrology_data["user_country"] = country

        return astrology_data  # Return updated JSON response
    
    except requests.exceptions.RequestException as e:
        st.error(f"API request failed: {e}")
        return {"error": "Failed to fetch astrology data"}

# Function to generate birth charts
def generate_birth_chart(name, year, month, day, hour, minute, city, country):
    print(f"🔍 Looking up: {city}, {country}")  # Debugging output

    # ✅ Fetch latitude & longitude using `geopy`
    lat, lon, timezone = get_location(city, country)

    if lat is None or lon is None:
        print("❌ Could not find location.")
        return None  # Stop if location is invalid

    print(f"✅ Using coordinates: {lat}, {lon}")

    try:
        # ✅ Pass lat/lon to Kerykeion
        subject = AstrologicalSubject(
            name=name,
            year=year,
            month=month,
            day=day,
            hour=hour,
            minute=minute,
            latitude=lat,
            longitude=lon,
            timezone=timezone
        )

        # ✅ Generate chart
        chart = KerykeionChartSVG(subject, chart_type="Natal")
        svg_data = chart.makeSVG()

        print("✅ Birth chart successfully generated!")  # Debugging
        return svg_data
    
    except Exception as e:
        print(f"❌ Error generating chart: {e}")
        return None

# Persistent token management
def update_tokens(change):
    st.session_state.token_count += change
    st.write(f"New token count: {st.session_state.token_count}")

# Streamlit app
def main():
    st.title("Horacle - Your Astro-Bot 🔮")

    astrology_data = None

    # Sidebar Navigation Menu
    st.sidebar.header("Navigation")
    page = st.sidebar.radio(
        "Go to", 
        ["Chat", "Current Astrology", "Charts", "Horoscope",  "Tokens"]
    )

    if page == "Chat":
        st.header("Chat with Horacle")
        user_input = st.text_input("You: ", "")
        if user_input:
            if st.session_state.token_count > 0:
                response = generate_response(user_input)
                st.write(f"Horacle: {response}")
                st.session_state.token_count -= 1
            else:
                st.write("You've used all your free tokens. Please purchase more.")

    elif page == "Current Astrology":
        st.header("🌍 Current Astrological Data")

        if st.button("Get Current Astrology"):
            astrology_data = fetch_current_astrology()  # ✅ Only assigns value if button clicked

        if astrology_data is not None:  # ✅ Safe check before using it
            if "error" not in astrology_data:
                user_city = astrology_data.get("user_city", "Unknown")
                user_country = astrology_data.get("user_country", "Unknown")

                # Convert the ISO timestamp to the desired format
                from datetime import datetime
                raw_datetime = astrology_data['data']['iso_formatted_local_datetime']
                formatted_datetime = datetime.strptime(raw_datetime, "%Y-%m-%dT%H:%M:%S%z").strftime("%I:%M %p %m/%d/%Y")

                st.write(f"📍 **Your Location:** {user_city}, {user_country}")
                st.write(f"🌞 **Sun Sign:** {astrology_data['data']['sun']['sign']} {astrology_data['data']['sun']['emoji']}")
                st.write(f"🌙 **Moon Sign:** {astrology_data['data']['moon']['sign']} {astrology_data['data']['moon']['emoji']}")
                st.write(f"⏳ **Date & Time:** {formatted_datetime}")  
            else:
                st.write("No astrology data available.")

    elif page == "Charts":
        st.header("Generate Astrology Charts")

        name = st.text_input("Name: ")
        year = st.number_input("Year of birth", min_value=1700, max_value=2100, value=1990)
        month = st.number_input("Month of birth", min_value=1, max_value=12, value=1)
        day = st.number_input("Day of birth", min_value=1, max_value=31, value=1)
        hour = st.number_input("Hour of birth", min_value=0, max_value=23, value=12)
        minute = st.number_input("Minute of birth", min_value=0, max_value=59, value=0)

        # ✅ Define city and country 
        city = st.text_input("City of birth", "New York")
        country = st.text_input("Country of birth:", "USA")
        
        if st.button("Generate Birth Chart"):
            chart_svg = generate_birth_chart(name, year, month, day, hour, minute, country)

            if chart_svg:
                st.image(chart_svg, format="svg")  # ✅ Show the chart
            else:
                st.error("Could not generate chart. Try a different city.")

    elif page == "Horoscope":
        st.header("Get Your Horoscope")
        name = st.text_input("Name: ")
        year = st.number_input("Year of birth", min_value=1900, max_value=2100, value=1990)
        month = st.number_input("Month of birth", min_value=1, max_value=12, value=1)
        day = st.number_input("Day of birth", min_value=1, max_value=31, value=1)
        hour = st.number_input("Hour of birth", min_value=0, max_value=23, value=12)
        minute = st.number_input("Minute of birth", min_value=0, max_value=59, value=0)
        city = st.text_input("City of birth", "New York")
        period = st.selectbox("Select period:", ["daily", "weekly", "monthly", "yearly"])

        if st.button("Get Horoscope"):
            with st.spinner("Fetching your horoscope..."):
                horoscope = fetch_horoscope(name, year, month, day, hour, minute, city, period)
                st.success("Horoscope retrieved!")

            if "error" in horoscope:
                st.write("Sorry, I couldn't fetch your horoscope. Please try again later.")
            else:
                st.write(f"Horacle: {horoscope.get('description', 'No horoscope available.')}")
           
    elif page == "Tokens":
        st.header("Token Management")
        st.write(f"Tokens remaining: {st.session_state.token_count}")
        if st.button("Buy 10 Tokens for $5"):
            st.session_state.token_count += 10
            st.write("10 tokens added to your account.")


if __name__ == "__main__":
    main()
