import streamlit as st
st.set_option("client.showErrorDetails", True)
import requests

# Access secrets safely with fallback/defaults
deepseek_api_key = st.secrets.get("DEEPSEEK_API_KEY", "")
astrology_api_key = st.secrets.get("ASTROLOGY_API_KEY", "")
database_url = st.secrets.get("DATABASE_URL", "")


# Streamlit app
def main():
    st.title("🧭 Horacle has loaded")
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

    if not all([deepseek_api_key, astrology_api_key, database_url]):
        st.error("Missing one or more required secrets! Please check Streamlit Cloud → Settings → Secrets.")


# Run the app
if __name__ == "__main__":
    main()