import streamlit as st
from astrology.birth_form import birth_data_form
from astrology.horoscope import fetch_horoscope_by_period
from astrology.charts import fetch_chart, build_chart_payload

# Show Python tracebacks if anything breaks
st.set_option("client.showErrorDetails", True)

def main():
    st.title("🔮 Horacle: Your Astrology Companion")
    st.sidebar.header("Navigation")
    page = st.sidebar.radio("Go to", ["Chat", "Charts", "Horoscope"])

    if page == "Chat":
        st.subheader("Chat with Horacle")
        user_input = st.text_input("You: ")
        if user_input:
            st.write(f"Horacle: You said **{user_input}**")

    elif page == "Charts":
        st.subheader("Generate Astrology Charts")
        st.info("Chart generation UI will go here.")

    elif page == "Horoscope":
        st.subheader("Get Your Horoscope")
        st.info("Horoscope UI will go here.")

if __name__ == "__main__":
    main()
