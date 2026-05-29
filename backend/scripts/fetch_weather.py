import csv
import os
from datetime import datetime

import requests

API_KEY = os.environ.get("OPENWEATHER_API_KEY", "")
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_weather(city="Cherrapunji"):
    """Fetch current weather for a city. Returns dict or None."""
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()

        if response.status_code == 200:
            weather_info = {
                "Date": datetime.now().strftime("%Y-%m-%d"),
                "City": city,
                "Temperature (°C)": data["main"]["temp"],
                "Humidity (%)": data["main"]["humidity"],
                "Wind Speed (m/s)": data["wind"]["speed"],
                "Pressure (hPa)": data["main"]["pressure"],
                "Weather Condition": data["weather"][0]["main"],
                "Description": data["weather"][0]["description"]
            }

            # Append to historical CSV without pulling in pandas on deployment.
            try:
                file_path = os.path.join(BASE_DIR, "data", "historical_weather.csv")
                file_exists = os.path.exists(file_path)
                with open(file_path, "a", newline="", encoding="utf-8") as handle:
                    writer = csv.DictWriter(handle, fieldnames=list(weather_info.keys()))
                    if not file_exists:
                        writer.writeheader()
                    writer.writerow(weather_info)
            except Exception:
                pass  # Don't fail if CSV write fails

            return weather_info
        else:
            print(f"❌ Error fetching weather data: {data}")
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

if __name__ == "__main__":
    get_weather()
