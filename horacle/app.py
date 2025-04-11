import streamlit as st
import requests
import logging
from astrology.birth_form import birth_data_form
from astrology.horoscope import fetch_horoscope_by_period
from astrology.deepseek import generate_response
from astrology.charts_local import generate_natal_chart_data  # ⬅️ New local chart

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
                st.markdown("### 🌠 Horacle says:")
                st.markdown(f"<div style='white-space: pre-wrap; word-wrap: break-word;'>{reply}</div>", unsafe_allow_html=True)
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

        if user_data and st.button("♈ Generate Natal Chart (Local)"):
            with st.spinner("Drawing your natal chart..."):
                try:
                    svg, planets, houses, aspects = generate_natal_chart_data(user_data)

                    # Show SVG
                    st.image(svg)

                    # Download button
                    st.download_button(
                        label="📥 Download Natal Chart SVG",
                        data=svg,
                        file_name="natal_chart.svg",
                        mime="image/svg+xml"
                    )

                    st.markdown("### 🌌 Planetary Positions")
                    for name, info in planets.items():
                        st.write(
                            f"**{name}**: {info['sign']} {info['degree']}° ({info['element']}), House {info['house']}"
                        )

                    st.markdown("### 🏠 Houses")
                    for i, deg in enumerate(houses, start=1):
                        st.write(f"House {i}: {deg:.2f}°")

                    st.markdown("### 🔗 Major Aspects")
                    for aspect in aspects:
                        st.write(f"{aspect[0]} {aspect[1]} {aspect[2]} (orb: {aspect[3]:.2f}°)")
                except Exception as e:
                    st.error(f"Failed to generate chart: {e}")

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
