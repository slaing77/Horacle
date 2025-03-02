from opencage.geocoder import OpenCageGeocode
import os
from kerykeion import AstrologicalSubject

# ✅ Set your OpenCage API key
OPENCAGE_API_KEY = "210eaaf240f14ce68ee7d1b20980f758"  # Replace with your key
geocoder = OpenCageGeocode(OPENCAGE_API_KEY)

def get_location(city, country):
    query = f"{city}, {country}"
    results = geocoder.geocode(query)

    if results:
        lat = results[0]['geometry']['lat']
        lng = results[0]['geometry']['lng']
        timezone = results[0]['annotations']['timezone']['name']
        print(f"✅ Location Found: {lat}, {lng}, {timezone}")
        return lat, lng, timezone
    else:
        print("❌ Location not found")
        return None, None, None

# ✅ Example Usage
city = "New York"
country = "USA"
lat, lng, timezone = get_location(city, country)

if lat and lng:
    # ✅ Pass manually to Kerykeion
    try:
        subject = AstrologicalSubject("Test User", 1990, 1, 1, 12, 0, city)
        print("✅ City recognized by Kerykeion!")
    except Exception as e:
        print(f"❌ Kerykeion did not recognize the city: {e}")
