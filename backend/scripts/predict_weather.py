import pandas as pd
import numpy as np
import joblib
import os
from datetime import datetime, timedelta

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_weather_forecast():
    """Return 7-day weather forecast as a list of dicts."""
    model_path = os.path.join(BASE_DIR, "models", "weather_forecast.pkl")
    data_path = os.path.join(BASE_DIR, "data", "historical_weather.csv")

    model = joblib.load(model_path)
    future_dates = [datetime.now() + timedelta(days=i) for i in range(1, 8)]
    future_days = [(date - datetime.now()).days for date in future_dates]

    df = pd.read_csv(data_path)
    median_temp = df["Temperature (°C)"].median()
    median_humidity = df["Humidity (%)"].median()
    median_wind_speed = df["Wind Speed (m/s)"].median()
    median_pressure = df["Pressure (hPa)"].median()

    input_data = pd.DataFrame({
        "Days": future_days,
        "Temperature (°C)": [median_temp] * 7,
        "Humidity (%)": [median_humidity] * 7,
        "Wind Speed (m/s)": [median_wind_speed] * 7,
        "Pressure (hPa)": [median_pressure] * 7,
    })

    predicted_temps = model.predict(input_data)

    forecast = []
    for i in range(7):
        temp = float(predicted_temps[i])
        # Derive simple condition from temperature
        if temp > 35:
            condition = "sunny"
            description = "Hot and sunny throughout the day."
        elif temp > 25:
            condition = "mostly-sunny"
            description = "Warm with mostly clear skies."
        elif temp > 18:
            condition = "partly-cloudy"
            description = "Pleasant with partly cloudy skies."
        elif temp > 10:
            condition = "cloudy"
            description = "Cool and cloudy throughout the day."
        else:
            condition = "light-rain"
            description = "Cold with possible light showers."

        forecast.append({
            "date": future_dates[i].strftime("%Y-%m-%d"),
            "temperature": round(temp, 2),
            "humidity": f"{int(median_humidity)}%",
            "wind": f"{median_wind_speed:.1f} m/s",
            "precipitation": f"{max(5, min(80, int(100 - temp * 2)))}%",
            "description": description,
            "condition": condition,
            "details": {
                "morning": f"{round(temp - 1.5, 1)}°C",
                "afternoon": f"{round(temp + 1.0, 1)}°C",
                "evening": f"{round(temp - 0.3, 1)}°C",
                "night": f"{round(temp - 2.0, 1)}°C"
            }
        })

    return forecast


if __name__ == "__main__":
    results = get_weather_forecast()
    print("\n7-Day Weather Forecast")
    for r in results:
        print(f"  {r['date']}: {r['temperature']}°C - {r['condition']}")
