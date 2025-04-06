import requests
import streamlit as st
import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)

# RapidAPI Astrology Service
API_BASE = "https://astrologer.p.rapidapi.com/api/v4"
API_HOST = "astrologer.p.rapidapi.com"
API_KEY = st.secrets.get("ASTROLOGY_API_KEY", "")

def build_chart_payload(user: dict, partner: dict = None) -> dict:
    """Builds payload for chart generation APIs."""
    base = {
        "name": str(user.get("name", "Unknown")),
        "year": int(user.get("year", 1990)),
        "month": int(user.get("month", 1)),
        "day": int(user.get("day", 1)),
        "hour": int(user.get("hour", 12)),
        "minute": int(user.get("minute", 0)),
        "city": str(user.get("city", "New York")),
        "country": str(user.get("country", "United States")),
    }

    # For synastry or relationship score
    if partner:
        base["partner"] = {
            "name": str(partner.get("name", "Partner")),
            "year": int(partner.get("year", 1990)),
            "month": int(partner.get("month", 1)),
            "day": int(partner.get("day", 1)),
            "hour": int(partner.get("hour", 12)),
            "minute": int(partner.get("minute", 0)),
            "city": str(partner.get("city", "New York")),
            "country": str(partner.get("country", "United States")),
        }

    return base


# Mapping of chart types to their respective API endpoints
CHART_API_MAP = {
    "birth-chart": "https://astrologer.p.rapidapi.com/api/v4/birth-chart",
    "transit-chart": "https://astrologer.p.rapidapi.com/api/v4/transit-chart",
    "synastry-chart": "https://astrologer.p.rapidapi.com/api/v4/synastry-chart",
    "relationship-score": "https://astrologer.p.rapidapi.com/api/v4/relationship-score"
}


def fetch_chart(payload: dict, chart_type: str) -> dict:
    url = CHART_API_MAP.get(chart_type)
    if not url:
        return {"error": f"Unknown chart type: {chart_type}"}

    headers = {
        "Content-Type": "application/json",
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "astrologer.p.rapidapi.com"
    }

    # Add chart type to payload
    payload["chart_type"] = chart_type

    # 🔍 Debug output to Streamlit
    st.subheader("📦 Payload Being Sent")
    st.json(payload)

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"error": f"Failed to fetch {chart_type}: {e}"}

