from astrology.charts import build_chart_payload, fetch_chart

USER = {
    "name": "Test", "year": 1990, "month": 1, "day": 1,
    "hour": 12, "minute": 0, "city": "London", "country": "UK"
}
PARTNER = {
    "name": "Partner", "year": 1991, "month": 2, "day": 2,
    "hour": 10, "minute": 30, "city": "Paris", "country": "FR"
}

def test_build_chart_payload_single():
    payload = build_chart_payload(USER)
    assert payload["name"] == "Test"

def test_build_chart_payload_dual():
    payload = build_chart_payload(USER, PARTNER)
    assert "person1" in payload and "person2" in payload
