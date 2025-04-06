import streamlit as st
import requests
from astrology.birth_form import birth_data_form
from astrology.horoscope import fetch_horoscope_by_period
from astrology.charts import fetch_chart, build_chart_payload
from astrology.deepseek import generate_response

# Enable error tracebacks
st.set_option("client.showErrorDetails", True)

# Ensure session variables exist
if "your_birth_data" not in st.session_state:
    st.session_state["your_birth_data"] = None

if "partner_birth_data" not in st.session_state:
    st.session_state["partner_birth_data"] = None

def main():
    st.set_page_config(page_title="Horacle 🔮", page_icon="🪐")
    st.title("🔮 Horacle — Your Astrology Assistant")

    # Sidebar Navigation
    st.sidebar.header("🌙 Navigation")
    page = st.sidebar.radio("Go to", ["Chat", "Charts", "Horoscope"])

    # 💬 Chat Page
    if page == "Chat":
        st.subheader("💬 Ask the Stars")
        st.markdown("Ask Horacle anything about astrology, your birth chart, or the cosmos.")

        prompt = st.text_area("You:", height=100)

        if st.button("Ask Horacle"):
            if prompt:
                with st.spinner("Consulting the stars..."):
                    user_data = st.session_state.get("your_birth_data", {})
                    context = ""
                    if user_data:
                        context = (
                            f"My birth details: {user_data.get('name')} born on "
                            f"{user_data.get('day')}/{user_data.get('month')}/{user_data.get('year')} at "
                            f"{user_data.get('hour')}:{user_data.get('minute')} in "
                            f"{user_data.get('city')}, {user_data.get('country')}.\n"
                        )
                    full_prompt = f"{context}{prompt}"
                    reply = generate_response(full_prompt)
                st.markdown(f"**Horacle says:** {reply}")
            else:
                st.warning("Please enter a question.")

    # 🪐 Charts Page
    elif page == "Charts":
        st.subheader("🪐 Generate Astrology Charts")

        # Retrieve or request user birth data
        user_data = st.session_state.get("your_birth_data", None)
        if not user_data:
            st.info("📋 Please enter your birth details:")
            user_data = birth_data_form("Your")
        else:
            st.success("✔️ Using your saved birth data.")

        # Optional partner birth data
        st.markdown("---")
        st.subheader("💑 Optional: Add Partner Info")
        partner_data = st.session_state.get("partner_birth_data", None)
        if not partner_data:
            partner_data = birth_data_form("Partner")

        st.markdown("---")
        st.subheader("📤 Chart Actions")

        # ♈ Natal Chart
        if user_data and st.button("♈ Generate Natal Chart"):
            with st.spinner("Drawing your natal chart..."):
                payload = build_chart_payload(user_data)
                st.json(payload)  # DEBUG: Show payload
                result = fetch_chart(payload, chart_type="birth-chart")
                if "chart_svg" in result:
                    st.image(result["chart_svg"])
                    if "chart_pdf" in result:
                        try:
                            pdf_data = requests.get(result["chart_pdf"], timeout=10).content
                            st.download_button(
                                label="📄 Download Natal Chart PDF",
                                data=pdf_data,
                                file_name="natal_chart.pdf",
                                mime="application/pdf"
                            )
                        except requests.RequestException:
                            st.warning("Could not download PDF chart.")
                else:
                    st.error(result.get("error", "Could not generate natal chart."))

        # 🌌 Transit Chart
        if user_data and st.button("🌌 Generate Transit Chart"):
            with st.spinner("Calculating current transits..."):
                payload = build_chart_payload(user_data)
                result = fetch_chart(payload, chart_type="transit-chart")
                if "chart_svg" in result:
                    st.image(result["chart_svg"])
                    if "chart_pdf" in result:
                        try:
                            pdf_data = requests.get(result["chart_pdf"], timeout=10).content
                            st.download_button(
                                label="📄 Download Transit Chart PDF",
                                data=pdf_data,
                                file_name="transit_chart.pdf",
                                mime="application/pdf"
                            )
                        except requests.RequestException:
                            st.warning("Could not download PDF chart.")
                else:
                    st.error(result.get("error", "Could not generate transit chart."))

        # ❤️ Synastry Chart
        if user_data and partner_data and st.button("❤️ Generate Synastry Chart"):
            with st.spinner("Mapping relationship energies..."):
                payload = build_chart_payload(user_data, partner_data)
                result = fetch_chart(payload, chart_type="synastry-chart")
                if "chart_svg" in result:
                    st.image(result["chart_svg"])
                    if "chart_pdf" in result:
                        try:
                            pdf_data = requests.get(result["chart_pdf"], timeout=10).content
                            st.download_button(
                                label="📄 Download Synastry Chart PDF",
                                data=pdf_data,
                                file_name="synastry_chart.pdf",
                                mime="application/pdf"
                            )
                        except requests.RequestException:
                            st.warning("Could not download PDF chart.")
                else:
                    st.error(result.get("error", "Could not generate synastry chart."))

        # 💞 Relationship Score
        if user_data and partner_data and st.button("💞 Check Relationship Score"):
            with st.spinner("Measuring compatibility..."):
                payload = build_chart_payload(user_data, partner_data)
                result = fetch_chart(payload, chart_type="relationship-score")
                if "score" in result and "max_score" in result:
                    st.metric(
                        label="💖 Relationship Score",
                        value=f"{result['score']} / {result['max_score']}"
                    )
                    st.write(result.get("result", "No detailed interpretation provided."))

                    try:
                        score_percent = int(result['score']) / int(result['max_score']) * 100
                        if score_percent > 80:
                            st.success("💘 Excellent match!")
                        elif score_percent > 50:
                            st.info("💞 Promising connection.")
                        else:
                            st.warning("⚠️ Room for growth.")
                    except (ValueError, ZeroDivisionError):
                        st.warning("⚠️ Could not interpret compatibility score.")
                else:
                    st.error(result.get("error", "Could not calculate relationship score."))

    # 🌟 Horoscope Page
    elif page == "Horoscope":
        st.subheader("🌟 Get Your Horoscope")

        zodiac_signs = [
            "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
            "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
        ]

        selected_sign = st.selectbox("🔭 Select your Zodiac Sign:", zodiac_signs)
        period = st.radio("🗓️ Choose a timeframe:", ["daily", "weekly", "monthly"])

        if st.button("🔮 Get Horoscope"):
            result = fetch_horoscope_by_period(selected_sign, period)
            if "error" in result:
                st.error(result["error"])
            else:
                st.markdown(f"### 🌠 {period.title()} Horoscope for {selected_sign}")
                st.write(result.get("horoscope"))

# 👇 Entry point
if __name__ == "__main__":
    main()
