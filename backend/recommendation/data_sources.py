"""
SmartCropX — Weather + Satellite helpers for crop recommendation.

Uses Open-Meteo (free, no key) for weather and a placeholder for NDVI.
"""

import logging
import random
import httpx

logger = logging.getLogger(__name__)

# ── Open-Meteo (free) ──────────────────────────────────────────────

OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"

FALLBACK_WEATHER = {
    "temperature_c": 28.0,
    "humidity_pct": 65.0,
    "rainfall_mm": 120.0,
    "source": "fallback-demo",
}


async def fetch_weather(lat: float, lon: float) -> dict:
    """Return temperature, humidity, rainfall for the given location.

    Falls back to demo values if the API is unreachable.
    """
    params = {
        "latitude": lat,
        "longitude": lon,
        "current_weather": "true",
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,relative_humidity_2m_max",
        "timezone": "auto",
        "forecast_days": 7,
    }
    try:
        async with httpx.AsyncClient(timeout=8.0) as client:
            resp = await client.get(OPEN_METEO_URL, params=params)
            resp.raise_for_status()
            data = resp.json()

        daily = data.get("daily", {})
        temps_max = daily.get("temperature_2m_max", [])
        temps_min = daily.get("temperature_2m_min", [])
        precip = daily.get("precipitation_sum", [])
        humid = daily.get("relative_humidity_2m_max", [])

        avg_temp = round(sum(temps_max) / len(temps_max), 1) if temps_max else 28.0
        avg_rain = round(sum(precip), 1) if precip else 0.0
        avg_humid = round(sum(humid) / len(humid), 1) if humid else 65.0

        return {
            "temperature_c": avg_temp,
            "humidity_pct": avg_humid,
            "rainfall_mm": avg_rain,
            "source": "open-meteo",
        }
    except Exception as exc:
        logger.warning(f"Open-Meteo fetch failed: {exc}; using fallback")
        return dict(FALLBACK_WEATHER)


# ── Satellite NDVI placeholder ──────────────────────────────────────

def get_satellite_ndvi(lat: float, lon: float) -> float:
    """Return a simulated NDVI value between 0 and 1.

    In production, replace with a real Sentinel-2 / MODIS API call.
    Simulation uses a seed derived from location so the same coords give
    consistent results within a session.
    """
    seed = int(abs(lat * 1000) + abs(lon * 1000)) % 10000
    rng = random.Random(seed)
    # Most agricultural land: NDVI 0.3 – 0.85
    return round(rng.uniform(0.30, 0.85), 2)
