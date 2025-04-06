import streamlit as st
import requests
import logging
from typing import Optional
from typing import Dict


DEEPSEEK_API_KEY = st.secrets.get("DEEPSEEK_API_KEY")
DEEPSEEK_URL = "https://api.deepseek.com/v1/chat/completions"

def generate_response(prompt: str) -> str:
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json",
    }

    data = {
        "model": "deepseek-chat",  # Make sure this matches their API
        "messages": [
            {"role": "system", "content": "You are an astrology expert."},
            {"role": "user", "content": prompt},
        ],
        "max_tokens": 300,
        "temperature": 0.7,
    }

    try:
        response = requests.post(DEEPSEEK_URL, headers=headers, json=data, timeout=60)
        response.raise_for_status()
        result: Dict = response.json()

        # ✅ Debug section (only runs if DEBUG = true in secrets.toml)
        if st.secrets.get("DEBUG", False):
            st.write("📤 Request sent:", data)
            st.write("📥 Response received:", result)

        # Defensive parsing
        return result.get("choices", [{}])[0].get("message", {}).get("content", "No response.")
    except Exception as e:
        return f"🕒 The astrology AI is taking too long to respond. Please try again later.\n\nError: {e}"
