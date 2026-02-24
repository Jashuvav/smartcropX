"""
SmartCropX — Rule-based crop recommendation engine.

Scores each candidate crop against weather, soil, NDVI, and NPK inputs
then returns the top-ranked results with human-readable explanations.
"""

from __future__ import annotations
import logging
from typing import List

logger = logging.getLogger(__name__)

# ═══════════════════════════════════════════════════════════════════
# Crop Knowledge-Base
# ═══════════════════════════════════════════════════════════════════
# Each entry defines the *ideal* growing conditions for a crop.
# Ranges are inclusive.  Score is penalised proportionally as the
# observed value departs from the ideal window.

CROP_DB: list[dict] = [
    {
        "name": "Rice",
        "temp_min": 20, "temp_max": 35,
        "rain_min": 100, "rain_max": 300,
        "humidity_min": 60, "humidity_max": 95,
        "ndvi_min": 0.35,
        "ph_min": 5.5, "ph_max": 7.5,
        "n_min": 60, "n_max": 120,
        "p_min": 20, "p_max": 60,
        "k_min": 20, "k_max": 60,
        "soils": ["alluvial", "clay", "black"],
    },
    {
        "name": "Wheat",
        "temp_min": 10, "temp_max": 25,
        "rain_min": 25, "rain_max": 100,
        "humidity_min": 40, "humidity_max": 70,
        "ndvi_min": 0.30,
        "ph_min": 6.0, "ph_max": 7.5,
        "n_min": 80, "n_max": 140,
        "p_min": 30, "p_max": 60,
        "k_min": 20, "k_max": 50,
        "soils": ["alluvial", "black", "loamy"],
    },
    {
        "name": "Maize",
        "temp_min": 18, "temp_max": 32,
        "rain_min": 50, "rain_max": 200,
        "humidity_min": 50, "humidity_max": 80,
        "ndvi_min": 0.35,
        "ph_min": 5.5, "ph_max": 7.5,
        "n_min": 80, "n_max": 150,
        "p_min": 30, "p_max": 70,
        "k_min": 20, "k_max": 60,
        "soils": ["alluvial", "loamy", "red", "sandy"],
    },
    {
        "name": "Cotton",
        "temp_min": 22, "temp_max": 35,
        "rain_min": 50, "rain_max": 150,
        "humidity_min": 40, "humidity_max": 70,
        "ndvi_min": 0.30,
        "ph_min": 6.0, "ph_max": 8.0,
        "n_min": 40, "n_max": 100,
        "p_min": 20, "p_max": 50,
        "k_min": 10, "k_max": 40,
        "soils": ["black", "alluvial", "red"],
    },
    {
        "name": "Sugarcane",
        "temp_min": 20, "temp_max": 38,
        "rain_min": 100, "rain_max": 250,
        "humidity_min": 55, "humidity_max": 90,
        "ndvi_min": 0.40,
        "ph_min": 6.0, "ph_max": 7.5,
        "n_min": 80, "n_max": 160,
        "p_min": 30, "p_max": 60,
        "k_min": 30, "k_max": 80,
        "soils": ["alluvial", "loamy", "black"],
    },
    {
        "name": "Tomato",
        "temp_min": 18, "temp_max": 30,
        "rain_min": 30, "rain_max": 120,
        "humidity_min": 40, "humidity_max": 75,
        "ndvi_min": 0.30,
        "ph_min": 6.0, "ph_max": 7.0,
        "n_min": 60, "n_max": 120,
        "p_min": 40, "p_max": 80,
        "k_min": 40, "k_max": 80,
        "soils": ["loamy", "alluvial", "red", "sandy"],
    },
    {
        "name": "Onion",
        "temp_min": 13, "temp_max": 28,
        "rain_min": 20, "rain_max": 80,
        "humidity_min": 40, "humidity_max": 70,
        "ndvi_min": 0.25,
        "ph_min": 6.0, "ph_max": 7.5,
        "n_min": 40, "n_max": 100,
        "p_min": 20, "p_max": 60,
        "k_min": 30, "k_max": 70,
        "soils": ["loamy", "alluvial", "sandy"],
    },
    {
        "name": "Banana",
        "temp_min": 22, "temp_max": 35,
        "rain_min": 80, "rain_max": 250,
        "humidity_min": 60, "humidity_max": 90,
        "ndvi_min": 0.40,
        "ph_min": 6.5, "ph_max": 7.5,
        "n_min": 80, "n_max": 160,
        "p_min": 30, "p_max": 60,
        "k_min": 60, "k_max": 120,
        "soils": ["loamy", "alluvial", "clay"],
    },
    {
        "name": "Carrot",
        "temp_min": 10, "temp_max": 25,
        "rain_min": 25, "rain_max": 80,
        "humidity_min": 40, "humidity_max": 70,
        "ndvi_min": 0.25,
        "ph_min": 6.0, "ph_max": 6.8,
        "n_min": 30, "n_max": 80,
        "p_min": 20, "p_max": 60,
        "k_min": 40, "k_max": 90,
        "soils": ["sandy", "loamy", "alluvial"],
    },
    {
        "name": "Groundnut",
        "temp_min": 22, "temp_max": 33,
        "rain_min": 40, "rain_max": 130,
        "humidity_min": 45, "humidity_max": 75,
        "ndvi_min": 0.30,
        "ph_min": 5.5, "ph_max": 7.0,
        "n_min": 20, "n_max": 60,
        "p_min": 20, "p_max": 50,
        "k_min": 20, "k_max": 50,
        "soils": ["red", "sandy", "loamy"],
    },
    {
        "name": "Soybean",
        "temp_min": 20, "temp_max": 30,
        "rain_min": 50, "rain_max": 150,
        "humidity_min": 50, "humidity_max": 80,
        "ndvi_min": 0.35,
        "ph_min": 6.0, "ph_max": 7.0,
        "n_min": 20, "n_max": 60,
        "p_min": 30, "p_max": 70,
        "k_min": 20, "k_max": 60,
        "soils": ["black", "alluvial", "loamy"],
    },
    {
        "name": "Potato",
        "temp_min": 12, "temp_max": 24,
        "rain_min": 30, "rain_max": 100,
        "humidity_min": 50, "humidity_max": 80,
        "ndvi_min": 0.30,
        "ph_min": 5.0, "ph_max": 6.5,
        "n_min": 60, "n_max": 120,
        "p_min": 40, "p_max": 80,
        "k_min": 60, "k_max": 120,
        "soils": ["loamy", "sandy", "alluvial", "red"],
    },
    {
        "name": "Millet",
        "temp_min": 25, "temp_max": 38,
        "rain_min": 20, "rain_max": 80,
        "humidity_min": 30, "humidity_max": 60,
        "ndvi_min": 0.20,
        "ph_min": 5.5, "ph_max": 7.5,
        "n_min": 20, "n_max": 60,
        "p_min": 10, "p_max": 40,
        "k_min": 10, "k_max": 40,
        "soils": ["sandy", "red", "laterite", "loamy"],
    },
    {
        "name": "Tea",
        "temp_min": 15, "temp_max": 28,
        "rain_min": 120, "rain_max": 350,
        "humidity_min": 70, "humidity_max": 95,
        "ndvi_min": 0.45,
        "ph_min": 4.5, "ph_max": 5.5,
        "n_min": 60, "n_max": 120,
        "p_min": 10, "p_max": 30,
        "k_min": 20, "k_max": 50,
        "soils": ["laterite", "red", "loamy"],
    },
    {
        "name": "Coffee",
        "temp_min": 15, "temp_max": 28,
        "rain_min": 100, "rain_max": 250,
        "humidity_min": 60, "humidity_max": 90,
        "ndvi_min": 0.40,
        "ph_min": 5.0, "ph_max": 6.5,
        "n_min": 40, "n_max": 100,
        "p_min": 10, "p_max": 30,
        "k_min": 20, "k_max": 50,
        "soils": ["laterite", "red", "loamy"],
    },
    {
        "name": "Chilli",
        "temp_min": 20, "temp_max": 35,
        "rain_min": 50, "rain_max": 150,
        "humidity_min": 50, "humidity_max": 80,
        "ndvi_min": 0.30,
        "ph_min": 6.0, "ph_max": 7.5,
        "n_min": 50, "n_max": 100,
        "p_min": 20, "p_max": 50,
        "k_min": 20, "k_max": 50,
        "soils": ["alluvial", "red", "black", "loamy", "sandy"],
    },
]


# ═══════════════════════════════════════════════════════════════════
# Scoring helpers
# ═══════════════════════════════════════════════════════════════════

def _range_score(value: float, lo: float, hi: float, weight: float = 1.0) -> tuple[float, str]:
    """Return (weighted score 0-1, short reason) for how well *value* fits [lo, hi]."""
    if lo <= value <= hi:
        return weight, "optimal"
    margin = (hi - lo) * 0.5 if (hi - lo) > 0 else 5.0
    if value < lo:
        dist = lo - value
    else:
        dist = value - hi
    raw = max(0.0, 1.0 - dist / margin)
    return round(raw * weight, 3), ("low" if value < lo else "high")


def score_crop(
    crop: dict,
    *,
    temp: float,
    rain: float,
    humidity: float,
    ndvi: float,
    soil: str,
    ph: float,
    n: float,
    p: float,
    k: float,
) -> dict | None:
    """Score a single crop entry. Returns dict with score + reasons, or None if totally unsuitable."""
    reasons: list[str] = []
    scores: list[float] = []

    # Soil match (binary, but high weight)
    soil_lower = soil.lower().strip()
    if soil_lower in crop["soils"]:
        scores.append(1.0)
        reasons.append(f"Soil ({soil}) is suitable")
    else:
        scores.append(0.0)
        reasons.append(f"Soil ({soil}) is not ideal")

    # Temperature
    s, tag = _range_score(temp, crop["temp_min"], crop["temp_max"])
    scores.append(s)
    if tag == "optimal":
        reasons.append(f"Temperature {temp}°C is optimal")
    else:
        reasons.append(f"Temperature {temp}°C is {tag}")

    # Rainfall
    s, tag = _range_score(rain, crop["rain_min"], crop["rain_max"])
    scores.append(s)
    if tag == "optimal":
        reasons.append(f"Rainfall {rain}mm is suitable")
    else:
        reasons.append(f"Rainfall {rain}mm is {tag}")

    # Humidity
    s, tag = _range_score(humidity, crop["humidity_min"], crop["humidity_max"])
    scores.append(s)
    if tag == "optimal":
        reasons.append(f"Humidity {humidity}% is good")

    # NDVI
    if ndvi >= crop["ndvi_min"]:
        scores.append(1.0)
        reasons.append(f"NDVI {ndvi} shows good vegetation")
    else:
        scores.append(0.3)
        reasons.append(f"NDVI {ndvi} is below threshold ({crop['ndvi_min']})")

    # pH
    s, tag = _range_score(ph, crop["ph_min"], crop["ph_max"])
    scores.append(s)
    if tag == "optimal":
        reasons.append(f"pH {ph} is within range")
    else:
        reasons.append(f"Soil pH {ph} is {tag}")

    # NPK
    for label, val, lo, hi in [
        ("Nitrogen", n, crop["n_min"], crop["n_max"]),
        ("Phosphorus", p, crop["p_min"], crop["p_max"]),
        ("Potassium", k, crop["k_min"], crop["k_max"]),
    ]:
        s, tag = _range_score(val, lo, hi, weight=0.8)
        scores.append(s)
        if tag != "optimal":
            reasons.append(f"{label} ({val}) is {tag}")

    final_score = round(sum(scores) / len(scores), 2) if scores else 0.0
    return {
        "crop": crop["name"],
        "score": final_score,
        "reason": " • ".join(reasons),
    }


def recommend_crops(
    *,
    temp: float,
    rain: float,
    humidity: float,
    ndvi: float,
    soil: str,
    ph: float,
    n: float,
    p: float,
    k: float,
    top_n: int = 3,
) -> List[dict]:
    """Return the top-N crops ranked by suitability score."""
    results = []
    for crop in CROP_DB:
        entry = score_crop(
            crop,
            temp=temp, rain=rain, humidity=humidity,
            ndvi=ndvi, soil=soil, ph=ph, n=n, p=p, k=k,
        )
        if entry:
            results.append(entry)

    results.sort(key=lambda r: r["score"], reverse=True)
    return results[:top_n]


# ═══════════════════════════════════════════════════════════════════
# Soil-only suitability
# ═══════════════════════════════════════════════════════════════════

SOIL_CROP_MAP: dict[str, list[dict]] = {
    "alluvial": [
        {"crop": "Rice", "base": 0.95},
        {"crop": "Wheat", "base": 0.92},
        {"crop": "Sugarcane", "base": 0.90},
        {"crop": "Maize", "base": 0.85},
        {"crop": "Banana", "base": 0.82},
        {"crop": "Tomato", "base": 0.80},
        {"crop": "Potato", "base": 0.78},
        {"crop": "Onion", "base": 0.75},
        {"crop": "Carrot", "base": 0.72},
        {"crop": "Chilli", "base": 0.78},
    ],
    "black": [
        {"crop": "Cotton", "base": 0.95},
        {"crop": "Soybean", "base": 0.92},
        {"crop": "Wheat", "base": 0.88},
        {"crop": "Sugarcane", "base": 0.85},
        {"crop": "Rice", "base": 0.80},
        {"crop": "Maize", "base": 0.78},
        {"crop": "Chilli", "base": 0.82},
    ],
    "red": [
        {"crop": "Groundnut", "base": 0.94},
        {"crop": "Potato", "base": 0.90},
        {"crop": "Millet", "base": 0.88},
        {"crop": "Maize", "base": 0.84},
        {"crop": "Tomato", "base": 0.80},
        {"crop": "Cotton", "base": 0.78},
        {"crop": "Coffee", "base": 0.75},
        {"crop": "Chilli", "base": 0.80},
    ],
    "laterite": [
        {"crop": "Tea", "base": 0.95},
        {"crop": "Coffee", "base": 0.93},
        {"crop": "Millet", "base": 0.78},
    ],
    "sandy": [
        {"crop": "Millet", "base": 0.92},
        {"crop": "Groundnut", "base": 0.90},
        {"crop": "Carrot", "base": 0.88},
        {"crop": "Onion", "base": 0.82},
        {"crop": "Maize", "base": 0.78},
        {"crop": "Potato", "base": 0.76},
        {"crop": "Tomato", "base": 0.74},
        {"crop": "Chilli", "base": 0.76},
    ],
    "clay": [
        {"crop": "Rice", "base": 0.95},
        {"crop": "Banana", "base": 0.82},
        {"crop": "Wheat", "base": 0.78},
    ],
    "loamy": [
        {"crop": "Wheat", "base": 0.95},
        {"crop": "Sugarcane", "base": 0.93},
        {"crop": "Tomato", "base": 0.92},
        {"crop": "Maize", "base": 0.90},
        {"crop": "Banana", "base": 0.88},
        {"crop": "Onion", "base": 0.85},
        {"crop": "Carrot", "base": 0.84},
        {"crop": "Potato", "base": 0.82},
        {"crop": "Soybean", "base": 0.80},
        {"crop": "Groundnut", "base": 0.78},
        {"crop": "Coffee", "base": 0.75},
        {"crop": "Tea", "base": 0.72},
        {"crop": "Chilli", "base": 0.80},
    ],
}


def _ph_factor(ph: float, crop_name: str) -> float:
    """Small adjustment based on pH suitability per crop."""
    for c in CROP_DB:
        if c["name"] == crop_name:
            if c["ph_min"] <= ph <= c["ph_max"]:
                return 1.0
            return 0.85
    return 0.90


def _npk_factor(n: float, p: float, k: float, crop_name: str) -> float:
    """Small adjustment based on NPK suitability."""
    for c in CROP_DB:
        if c["name"] == crop_name:
            in_range = 0
            total = 3
            if c["n_min"] <= n <= c["n_max"]:
                in_range += 1
            if c["p_min"] <= p <= c["p_max"]:
                in_range += 1
            if c["k_min"] <= k <= c["k_max"]:
                in_range += 1
            return 0.7 + 0.3 * (in_range / total)
    return 0.85


def soil_suitability(
    *,
    soil_type: str,
    ph: float,
    n: float,
    p: float,
    k: float,
    top_n: int = 5,
) -> List[dict]:
    """Return top-N crops ranked by soil suitability."""
    soil_key = soil_type.lower().strip()
    entries = SOIL_CROP_MAP.get(soil_key, [])

    if not entries:
        # If soil not found, score all crops from CROP_DB with soil penalty
        entries = [{"crop": c["name"], "base": 0.50} for c in CROP_DB]

    results = []
    for e in entries:
        base = e["base"]
        ph_adj = _ph_factor(ph, e["crop"])
        npk_adj = _npk_factor(n, p, k, e["crop"])
        score = round(base * ph_adj * npk_adj, 2)
        results.append({"crop": e["crop"], "suitability": score})

    results.sort(key=lambda r: r["suitability"], reverse=True)
    return results[:top_n]
