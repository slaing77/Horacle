import streamlit as st
import requests

# Access secrets
deepseek_api_key = st.secrets["DEEPSEEK_API_KEY"]
kerykeion_api_key = st.secrets["KERYKEION_API_KEY"]
database_url = st.secrets["DATABASE_URL"]

# Streamlit app
def main():
    st.title("Horacle — Astrology Chatbot")
    st.sidebar.header("Navigation")
    page = st.sidebar.radio("Go to", ["Chat", "Charts", "Horoscope"])

    if page == "Chat":
        st.header("Chat with Horacle")
        if user_input := st.text_input("You: ", ""):
            st.write(f"Horacle: You said: {user_input}")

    elif page == "Charts":
        st.header("Generate Astrology Charts")
        st.write("Chart generation will go here.")

    elif page == "Horoscope":
        st.header("Get Your Personalized Horoscope")
        st.write("Horoscope generation will go here.")

# Run the app
if __name__ == "__main__":
    main()