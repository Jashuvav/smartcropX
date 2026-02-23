import requests
import os
import pandas as pd
from datetime import datetime

API_KEY = os.environ.get("OPENWEATHER_API_KEY", "972c0e29b63fc85cd2fc3e1a945d8111")
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

            # Append to historical CSV
            try:
                df = pd.DataFrame([weather_info])
                file_path = os.path.join(BASE_DIR, "data", "historical_weather.csv")
                if os.path.exists(file_path):
                    df.to_csv(file_path, mode="a", header=False, index=False)
                else:
                    df.to_csv(file_path, index=False)
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
