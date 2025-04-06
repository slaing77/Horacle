import pytest
from astrology.horoscope import fetch_horoscope_by_period

@pytest.mark.parametrize("period", ["daily", "weekly", "monthly"])
def test_fetch_horoscope_success(mock_requests_get, period):
    mock_requests_get.return_value.status_code = 200
    mock_requests_get.return_value.json.return_value = {
        "data": {"horoscope_data": "Good things are coming your way!"}
    }
    result = fetch_horoscope_by_period("leo", period)
    assert result["zodiacSign"] == "leo"
    assert "good" in result["horoscope"].lower()
