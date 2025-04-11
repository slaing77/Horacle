# horacle/astrology/charts_local.py

from kerykeion.charts import Chart
from kerykeion.charts_utilities import kerykeion_chart_svg
from typing import Dict, Tuple, List
from io import BytesIO


def generate_natal_chart_data(user_data: Dict) -> Tuple[bytes, Dict, List, List]:
    """
    Generate a natal chart and return SVG, planets, houses, and aspects.

    Args:
        user_data (Dict): Birth data.

    Returns:
        Tuple:
            - SVG image (bytes)
            - Planetary positions (Dict)
            - House positions (List)
            - Aspects (List of Tuples)
    """
    chart = Chart(
        name=user_data.get("name", "User"),
        year=int(user_data["year"]),
        month=int(user_data["month"]),
        day=int(user_data["day"]),
        hour=int(user_data["hour"]),
        minute=int(user_data["minute"]),
        city=user_data["city"],
        country=user_data["country"]
    )

    # Generate SVG
    svg = kerykeion_chart_svg(chart)

    # Extract core data
    planets = {
        planet.name: {
            "sign": planet.sign,
            "degree": round(planet.longitude, 2),
            "element": planet.element,
            "house": planet.house,
        }
        for planet in chart.planets.values()
    }

    houses = chart.houses  # list of degrees
    aspects = chart.aspects  # list of (planet1, aspect, planet2, orb)

    return svg, planets, houses, aspects
