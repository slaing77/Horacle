import requests
from typing import Dict

DAILY_URL = "https://horoscope-app-api.vercel.app/api/v1/get-horoscope/daily"
WEEKLY_URL = "https://horoscope-app-api.vercel.app/api/v1/get-horoscope/weekly"
MONTHLY_URL = "https://horoscope-app-api.vercel.app/api/v1/get-horoscope/monthly"

URL_MAP = {"daily": DAILY_URL, "weekly": WEEKLY_URL, "monthly": MONTHLY_URL}

def fetch_horoscope_by_period(sign: str, period: str) -> Dict[str, str]:
    url = URL_MAP.get(period.lower())
    if not url:
        return {"error": f"Invalid period: {period}"}
    try:
        response = requests.get(url, headers={"Accept": "application/json"}, params={"sign": sign.lower()})
        response.raise_for_status()
        data = response.json()
        return {
            "zodiacSign": sign,
            "horoscope": data.get("data", {}).get("horoscope_data") or data.get("horoscope", "No data found")
        }
    except requests.RequestException as e:
        return {"error": f"Failed to fetch horoscope: {e}"}
