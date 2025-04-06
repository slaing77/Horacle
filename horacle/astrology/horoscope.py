import requests
import logging
from typing import Literal, Dict

logger = logging.getLogger(__name__)

DAILY_URL = "https://horoscope-app-api.vercel.app/api/v1/get-horoscope/daily"
WEEKLY_URL = "https://horoscope-app-api.vercel.app/api/v1/get-horoscope/weekly"
MONTHLY_URL = "https://horoscope-app-api.vercel.app/api/v1/get-horoscope/monthly"

URL_MAP: Dict[str, str] = {
    "daily": DAILY_URL,
    "weekly": WEEKLY_URL,
    "monthly": MONTHLY_URL,
}

def fetch_horoscope_by_period(sign: str, period: Literal["daily", "weekly", "monthly"]) -> Dict[str, str]:
    """Fetch horoscope data for a given zodiac sign and time period.

    Args:
        sign (str): The zodiac sign (e.g., 'Aries').
        period (str): 'daily', 'weekly', or 'monthly'.

    Returns:
        dict: Dictionary with 'zodiacSign' and 'horoscope' or error message.
    """
    url = URL_MAP.get(period.lower())
    if not url:
        return {"error": f"❌ Invalid period: {period}. Choose daily, weekly, or monthly."}

    headers = {
        "Accept": "application/json",
        "User-Agent": "HoracleBot/1.0"
    }

    params = {"sign": sign.lower()}

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        # Try multiple formats to support all API styles
        horoscope_text = (
            data.get("data", {}).get("horoscope_data") or
            data.get("horoscope") or
            "⚠️ No horoscope available from the API."
        )

        return {
            "zodiacSign": sign,
            "horoscope": horoscope_text
        }

    except requests.RequestException as e:
        logger.error("Horoscope API error: %s", e)
        return {"error": f"🛑 Failed to fetch {period} horoscope: {e}"}
