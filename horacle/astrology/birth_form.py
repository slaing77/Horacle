import streamlit as st

def birth_data_form(label_prefix: str = "Your") -> dict:
    """Displays a form for entering birth data and stores it in session state."""
    st.subheader(f"{label_prefix} Birth Information")

    with st.form(f"{label_prefix.lower()}_birth_form"):
        name = st.text_input(f"{label_prefix} Name", value=st.session_state.get(f"{label_prefix}_name", ""))
        year = st.number_input("Year", min_value=1900, max_value=2100, value=1990)
        month = st.number_input("Month", min_value=1, max_value=12, value=1)
        day = st.number_input("Day", min_value=1, max_value=31, value=1)
        hour = st.number_input("Hour", min_value=0, max_value=23, value=12)
        minute = st.number_input("Minute", min_value=0, max_value=59, value=0)
        city = st.text_input("City of Birth", value=st.session_state.get(f"{label_prefix}_city", ""))
        country = st.text_input("Country of Birth", value=st.session_state.get(f"{label_prefix}_country", ""))

        submitted = st.form_submit_button("Save Birth Data")
        if submitted:
            birth_data = {
                "name": name, "year": int(year), "month": int(month), "day": int(day),
                "hour": int(hour), "minute": int(minute), "city": city, "country": country
            }
            st.session_state[f"{label_prefix.lower()}_birth_data"] = birth_data
            st.success(f"{label_prefix} birth data saved.")
            return birth_data

    return st.session_state.get(f"{label_prefix.lower()}_birth_data", {})
