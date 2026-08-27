"""
Weather Forecast App
---------------------
A command-line Python app that fetches live weather data from a public
REST API (Open-Meteo - free, no API key required) and displays city-wise
forecasts: temperature, humidity, and conditions.

Concepts used (good talking points for interviews):
    - Calling a public REST API using the `requests` library
    - Parsing JSON responses
    - Exception handling for invalid city names and network failures
    - Basic functions and clean program structure

Run it with:
    pip install requests
    python weather_app.py
"""

import requests

GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

# WMO weather codes -> human-readable conditions
# (Open-Meteo returns a numeric code; this maps it to plain text)
WEATHER_CODES = {
    0: "Clear sky",
    1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
    45: "Fog", 48: "Depositing rime fog",
    51: "Light drizzle", 53: "Moderate drizzle", 55: "Dense drizzle",
    61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
    71: "Slight snow", 73: "Moderate snow", 75: "Heavy snow",
    80: "Slight rain showers", 81: "Moderate rain showers", 82: "Violent rain showers",
    95: "Thunderstorm", 96: "Thunderstorm with slight hail", 99: "Thunderstorm with heavy hail",
}


def get_coordinates(city_name):
    """Look up latitude/longitude for a city name.
    Returns a dict with name, country, lat, lon - or None if not found."""
    try:
        response = requests.get(
            GEOCODE_URL,
            params={"name": city_name, "count": 1},
            timeout=10,
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"Could not reach the geocoding service: {e}")

    data = response.json()
    results = data.get("results")
    if not results:
        return None  # invalid / unknown city name

    place = results[0]
    return {
        "name": place["name"],
        "country": place.get("country", ""),
        "lat": place["latitude"],
        "lon": place["longitude"],
    }


def get_weather(lat, lon):
    """Fetch current weather for the given coordinates.
    Returns a dict with temperature, humidity, and condition text."""
    try:
        response = requests.get(
            FORECAST_URL,
            params={
                "latitude": lat,
                "longitude": lon,
                "current": "temperature_2m,relative_humidity_2m,weather_code",
            },
            timeout=10,
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"Could not reach the weather service: {e}")

    data = response.json()
    current = data.get("current")
    if not current:
        raise ValueError("Unexpected response from weather service.")

    code = current.get("weather_code")
    return {
        "temperature": current.get("temperature_2m"),
        "humidity": current.get("relative_humidity_2m"),
        "condition": WEATHER_CODES.get(code, "Unknown"),
    }


def show_forecast(city_name):
    """Look up a city and print its current weather. Handles all errors
    gracefully so the app never crashes on bad input or a dropped connection."""
    try:
        place = get_coordinates(city_name)
        if place is None:
            print(f"  Couldn't find a city named '{city_name}'. Please check the spelling.\n")
            return

        weather = get_weather(place["lat"], place["lon"])

        location_label = place["name"]
        if place["country"]:
            location_label += f", {place['country']}"

        print(f"\nWeather in {location_label}")
        print("-" * (len(location_label) + 11))
        print(f"  Temperature : {weather['temperature']}°C")
        print(f"  Humidity    : {weather['humidity']}%")
        print(f"  Condition   : {weather['condition']}\n")

    except ConnectionError as e:
        print(f"  Network error: {e}")
        print("  Please check your internet connection and try again.\n")
    except ValueError as e:
        print(f"  {e}\n")


def main():
    print("=" * 50)
    print(" WEATHER FORECAST APP")
    print(" (type 'quit' to exit)")
    print("=" * 50)

    while True:
        city = input("\nEnter a city name: ").strip()
        if city.lower() in ("quit", "exit", "q"):
            print("Goodbye!")
            break
        if not city:
            print("  Please type a city name.")
            continue

        show_forecast(city)


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n\nGoodbye!")
