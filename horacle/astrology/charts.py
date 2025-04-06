import requests
import streamlit as st
from typing import Dict, Any

RAPIDAPI_KEY = st.secrets.get("ASTROLOGY_API_KEY", "")
RAPIDAPI_HOST = "astrologer.p.rapidapi.com"

HEADERS = {
    "X-RapidAPI-Key": RAPIDAPI_KEY,
    "X-RapidAPI-Host": RAPIDAPI_HOST,
    "Content-Type": "application/json"
}

ENDPOINTS = {
    "Natal Chart": "https://astrologer.p.rapidapi.com/api/v4/birth-chart",
    "Transit Chart": "https://astrologer.p.rapidapi.com/api/v4/transit-chart",
    "Synastry Chart": "https://astrologer.p.rapidapi.com/api/v4/synastry-chart",
    "Relationship Score": "https://astrologer.p.rapidapi.com/api/v4/relationship-score",
}

def fetch_chart(chart_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
    url = ENDPOINTS.get(chart_type)
    if not url:
        return {"error": f"Unsupported chart type: {chart_type}"}
    try:
        response = requests.post(url, headers=HEADERS, json=data)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"error": f"Failed to fetch {chart_type}: {e}"}

def build_chart_payload(user: dict, partner: dict = None) -> dict:
    base = {
        "name": user["name"], "year": user["year"], "month": user["month"],
        "day": user["day"], "hour": user["hour"], "minute": user["minute"],
        "city": user["city"], "country": user["country"]
    }
    if partner:
        return {"person1": base, "person2": partner}
    return base
