import os
from fetch_geonames import FetchGeonames  # ✅ Import your custom GeoNames handler
from kerykeion import AstrologicalSubject

# ✅ Set your custom GeoNames username
username = "sr_laing"  # Replace with your actual GeoNames username

# ✅ Try fetching city data
geonames = FetchGeonames("New York", "US", username)
city_data = geonames.get_serialized_data()
print("🔍 GeoNames API Response:", city_data)

if "lat" in city_data and "lng" in city_data:
    print("✅ City recognized by GeoNames!")
    
    # ✅ Now test with Kerykeion
    try:
        subject = AstrologicalSubject("Test User", 1990, 1, 1, 12, 0, "New York, USA")
        print("✅ City recognized by Kerykeion!")
    except Exception as e:
        print(f"❌ Kerykeion did not recognize the city: {e}")
else:
    print("❌ GeoNames did not return location data.")


