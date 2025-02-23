import streamlit as st
import requests
from kerykeion import AstrologicalSubject, KerykeionChartSVG
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import psycopg2
from datetime import datetime

# Access secrets
deepseek_api_key = st.secrets["DEEPSEEK_API_KEY"]
kerykeion_api_key = st.secrets["KERYKEION_API_KEY"]
database_url = st.secrets["DATABASE_URL"]

# Initialize session state for user data and token count
if "user_data" not in st.session_state:
    st.session_state.user_data = {}
if "token_count" not in st.session_state:
    st.session_state.token_count = 5  # Free threshold: 5 tokens

# Function to generate responses using DeepSeek-V3
def generate_response(prompt):
    headers = {
        "Authorization": f"Bearer {deepseek_api_key}",
        "Content-Type": "application/json",
    }
    data = {
        "model": "deepseek-v3",
        "messages": [
            {"role": "system", "content": "You are an astrology expert. Provide accurate and insightful responses in a conversational tone."},
            {"role": "user", "content": prompt},
        ],
        "max_tokens": 200,
        "temperature": 0.7,
    }
    response = requests.post("https://api.deepseek.com/v1/chat/completions", headers=headers, json=data)
    return response.json()['choices'][0]['message']['content']

# Function to fetch horoscope from Kerykeion API
def fetch_horoscope(name, year, month, day, hour, minute, city, period="daily"):
    url = "https://api.kerykeion.net/generate-horoscope"
    headers = {
        "Authorization": f"Bearer {kerykeion_api_key}",
        "Content-Type": "application/json",
    }
    data = {
        "name": name,
        "year": year,
        "month": month,
        "day": day,
        "hour": hour,
        "minute": minute,
        "city": city,
        "period": period,
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to fetch horoscope"}

# Function to generate a birth chart
def generate_birth_chart(name, year, month, day, hour, minute, city):
    subject = AstrologicalSubject(name, year, month, day, hour, minute, city)
    chart = KerykeionChartSVG(subject)
    chart.makeSVG()
    return f"{subject.name}_chart.svg"

# Function to generate a transit chart
def generate_transit_chart(name, year, month, day, hour, minute, city):
    subject = AstrologicalSubject(name, year, month, day, hour, minute, city)
    chart = KerykeionChartSVG(subject, chart_type="Transit")
    chart.makeSVG()
    return f"{subject.name}_transit_chart.svg"

# Function to generate a compatibility chart
def generate_compatibility_chart(name1, name2, year1, month1, day1, hour1, minute1, city1,
                                year2, month2, day2, hour2, minute2, city2):
    subject1 = AstrologicalSubject(name1, year1, month1, day1, hour1, minute1, city1)
    subject2 = AstrologicalSubject(name2, year2, month2, day2, hour2, minute2, city2)
    chart = KerykeionChartSVG(subject1, second_obj=subject2, chart_type="Composite")
    chart.makeSVG()
    return f"{name1}_{name2}_compatibility_chart.svg"

# Function to generate a PDF report
def generate_pdf(filename, content):
    c = canvas.Canvas(filename, pagesize=letter)
    c.drawString(100, 750, content)
    c.save()

# Function to deduct tokens
def deduct_tokens(user_id, tokens):
    conn = psycopg2.connect(database_url)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE users
        SET tokens = tokens - %s
        WHERE id = %s
    """, (tokens, user_id))
    conn.commit()
    conn.close()

# Streamlit app
def main():
    st.title("Horacle — Astrology Chatbot")
    st.sidebar.header("Navigation")
    page = st.sidebar.radio("Go to", ["Chat", "Charts", "Horoscope", "Tokens"])

    if page == "Chat":
        st.header("Chat with Horacle")
        user_input = st.text_input("You: ", "")
        if user_input:
            if st.session_state.token_count > 0:
                response = generate_response(user_input)
                st.write(f"Horacle: {response}")
                st.session_state.token_count -= 1
            else:
                st.write("You've used all your free tokens. Please purchase more to continue.")

    elif page == "Charts":
        st.header("Generate Astrology Charts")
        name = st.text_input("Name: ")
        year = st.number_input("Year of birth (e.g., 1990): ", min_value=1900, max_value=2100, value=1990)
        month = st.number_input("Month of birth (1-12): ", min_value=1, max_value=12, value=1)
        day = st.number_input("Day of birth (1-31): ", min_value=1, max_value=31, value=1)
        hour = st.number_input("Hour of birth (0-23): ", min_value=0, max_value=23, value=12)
        minute = st.number_input("Minute of birth (0-59): ", min_value=0, max_value=59, value=0)
        city = st.text_input("City of birth: ", "New York")
        if st.button("Generate Birth Chart"):
            chart_file = generate_birth_chart(name, year, month, day, hour, minute, city)
            st.write(f"Birth chart generated: {chart_file}")
            st.image(chart_file)
        if st.button("Generate Transit Chart"):
            chart_file = generate_transit_chart(name, year, month, day, hour, minute, city)
            st.write(f"Transit chart generated: {chart_file}")
            st.image(chart_file)

    elif page == "Horoscope":
        st.header("Get Your Personalized Horoscope")
        name = st.text_input("Name: ")
        year = st.number_input("Year of birth (e.g., 1990): ", min_value=1900, max_value=2100, value=1990)
        month = st.number_input("Month of birth (1-12): ", min_value=1, max_value=12, value=1)
        day = st.number_input("Day of birth (1-31): ", min_value=1, max_value=31, value=1)
        hour = st.number_input("Hour of birth (0-23): ", min_value=0, max_value=23, value=12)
        minute = st.number_input("Minute of birth (0-59): ", min_value=0, max_value=59, value=0)
        city = st.text_input("City of birth: ", "New York")
        period = st.selectbox("Select period:", ["daily", "weekly", "monthly", "yearly"])
        if st.button("Get Horoscope"):
            horoscope = fetch_horoscope(name, year, month, day, hour, minute, city, period)
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

# Run the app
if __name__ == "__main__":
    main()