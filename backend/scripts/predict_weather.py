import csv
import os
from statistics import median
from datetime import datetime, timedelta

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_weather_forecast():
    """Return 7-day weather forecast as a list of dicts."""
    data_path = os.path.join(BASE_DIR, "data", "historical_weather.csv")
    future_dates = [datetime.now() + timedelta(days=i) for i in range(1, 8)]

    with open(data_path, newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        return []

    temperatures = [float(row["Temperature (°C)"]) for row in rows if row.get("Temperature (°C)")]
    humidities = [float(row["Humidity (%)"]) for row in rows if row.get("Humidity (%)")]
    wind_speeds = [float(row["Wind Speed (m/s)"]) for row in rows if row.get("Wind Speed (m/s)")]
    pressures = [float(row["Pressure (hPa)"]) for row in rows if row.get("Pressure (hPa)")]

    median_temp = float(median(temperatures))
    median_humidity = float(median(humidities))
    median_wind_speed = float(median(wind_speeds))
    median_pressure = float(median(pressures))

    forecast = []
    for i in range(7):
        temp = round(median_temp + ((i - 3) * 0.4), 2)
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
