import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def check_weather_alerts():
    """Check latest weather data for extreme conditions. Returns list of alert strings."""
    alerts = []
    try:
        csv_path = os.path.join(BASE_DIR, "data", "historical_weather.csv")
        weather_df = pd.read_csv(csv_path)
        if weather_df.empty:
            return alerts
        weather = weather_df.iloc[-1]  # use latest row
    except Exception:
        return alerts

    condition = str(weather.get("Weather Condition", "")).lower()
    temp = float(weather.get("Temperature (°C)", 0))
    humidity = float(weather.get("Humidity (%)", 50))
    wind = float(weather.get("Wind Speed (m/s)", 0))

    if condition in ["storm", "thunderstorm", "hurricane"]:
        alerts.append("Storm Alert! Take precautions.")
    if temp > 40 and humidity < 25:
        alerts.append("Drought Alert! Extremely hot and dry conditions.")
    if condition in ["rain", "heavy rain", "drizzle"] and humidity > 90:
        alerts.append("Flood Alert! Heavy rain detected. Stay safe.")
    if wind > 15:
        alerts.append("High Wind Speed Alert! Secure loose objects.")

    return alerts
