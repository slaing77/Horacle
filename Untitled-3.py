import os
from kerykeion import AstrologicalSubject

# ✅ Force Kerykeion to use your GeoNames username
os.environ["GEONAMES_USERNAME"] = "sr_laing"

def test_city_lookup(city, country):
    """Check if Kerykeion recognizes a city."""
    try:
        subject = AstrologicalSubject("Test User", 1990, 1, 1, 12, 0, f"{city}, {country}")
        print(f"✅ {city}, {country} is recognized by Kerykeion!")
    except Exception as e:
        print(f"❌ {city}, {country} is NOT recognized by Kerykeion. Error: {e}")

# ✅ Test with different cities
test_city_lookup("New York", "USA")
test_city_lookup("New York City", "USA")  # 🔹 Try different formats
test_city_lookup("London", "UK")
test_city_lookup("Paris", "France")
test_city_lookup("Mumbai", "India")
test_city_lookup("Tokyo", "Japan")
