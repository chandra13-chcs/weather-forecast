# Weather Forecast App (Python)

A command-line app that fetches **live weather data** from a public REST API
and displays temperature, humidity, and conditions for any city you enter.

Uses [Open-Meteo](https://open-meteo.com/) — a free public weather API that
requires **no sign-up or API key**, so you can run this immediately.

## Features

- Look up current weather for any city by name
- Displays temperature, humidity, and weather condition
- Handles invalid/misspelled city names gracefully
- Handles network failures (timeouts, no internet) without crashing
- Runs in a loop so you can check multiple cities; type `quit` to exit

## Tech Stack

- Python 3
- [`requests`](https://pypi.org/project/requests/) — to call the REST API
- Two public endpoints:
  - Geocoding API — converts a city name into latitude/longitude
  - Forecast API — returns current weather for those coordinates

## How to Run

```bash
pip install requests
python weather_app.py
```

Example:

```
Enter a city name: Hyderabad

Weather in Hyderabad, India
---------------------------
  Temperature : 31.2°C
  Humidity    : 55%
  Condition   : Partly cloudy

Enter a city name: quit
Goodbye!
```

## Project Structure

```
weather_app/
├── weather_app.py   # Main application
└── README.md
```

## Possible Extensions

- Add a 5-day forecast view (Open-Meteo supports this)
- Add unit conversion (Celsius/Fahrenheit toggle)
- Build a simple GUI with Tkinter
- Cache recent city lookups to reduce repeated API calls
