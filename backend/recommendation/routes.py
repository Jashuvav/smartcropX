"""
SmartCropX — Recommendation API routes.

POST /api/recommend/crop      — full crop recommendation (weather + satellite + soil + NPK)
POST /api/recommend/soil      — soil-only suitability ranking
GET  /api/recommend/health    — module health check
"""

import logging
import time
import uuid
import traceback

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from community.database import get_db
from .schemas import (
    CropRecommendInput,
    SoilRecommendInput,
    CropRecommendResponse,
    SoilRecommendResponse,
)
from .data_sources import fetch_weather, get_satellite_ndvi
from .engine import recommend_crops, soil_suitability
from .models import CropRecommendationHistory

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/recommend", tags=["Recommendation"])


# ── Health ──────────────────────────────────────────────────────────

@router.get("/health")
def recommend_health():
    return {"status": "ok", "module": "crop-recommendation"}


# ── Crop Recommendation ────────────────────────────────────────────

@router.post("/crop", response_model=CropRecommendResponse)
async def recommend_crop(payload: CropRecommendInput, db: Session = Depends(get_db)):
    request_id = uuid.uuid4().hex[:12]
    t0 = time.perf_counter()
    logger.info(f"[recommend:{request_id}] crop request lat={payload.latitude} lon={payload.longitude} soil={payload.soil_type}")

    try:
        # 1. Fetch weather
        weather = await fetch_weather(payload.latitude, payload.longitude)

        # 2. Get NDVI
        ndvi = get_satellite_ndvi(payload.latitude, payload.longitude)

        # 3. Run scoring engine
        ranked = recommend_crops(
            temp=weather["temperature_c"],
            rain=weather["rainfall_mm"],
            humidity=weather["humidity_pct"],
            ndvi=ndvi,
            soil=payload.soil_type,
            ph=payload.ph,
            n=payload.nitrogen,
            p=payload.phosphorus,
            k=payload.potassium,
            top_n=3,
        )

        # 4. Persist to history (fire & forget, don't let DB errors block response)
        try:
            record = CropRecommendationHistory(
                latitude=payload.latitude,
                longitude=payload.longitude,
                district=payload.district,
                soil_type=payload.soil_type,
                ph=payload.ph,
                nitrogen=payload.nitrogen,
                phosphorus=payload.phosphorus,
                potassium=payload.potassium,
                recommended_crops=[r for r in ranked],
                weather_summary=weather,
                ndvi=ndvi,
            )
            db.add(record)
            db.commit()
        except Exception as db_err:
            logger.warning(f"[recommend:{request_id}] DB save failed: {db_err}")
            db.rollback()

        latency = round((time.perf_counter() - t0) * 1000, 1)
        logger.info(f"[recommend:{request_id}] done in {latency}ms — top crop={ranked[0]['crop'] if ranked else 'none'}")

        return {
            "recommended_crops": ranked,
            "weather_summary": weather,
            "ndvi": ndvi,
        }

    except Exception as exc:
        logger.error(f"[recommend:{request_id}] ERROR: {exc}")
        logger.error(traceback.format_exc())
        return JSONResponse(status_code=500, content={"status": "error", "detail": str(exc)})


# ── Soil Suitability ───────────────────────────────────────────────

@router.post("/soil", response_model=SoilRecommendResponse)
async def recommend_soil(payload: SoilRecommendInput):
    request_id = uuid.uuid4().hex[:12]
    t0 = time.perf_counter()
    logger.info(f"[soil-rec:{request_id}] soil={payload.soil_type} ph={payload.ph}")

    try:
        ranked = soil_suitability(
            soil_type=payload.soil_type,
            ph=payload.ph,
            n=payload.nitrogen,
            p=payload.phosphorus,
            k=payload.potassium,
            top_n=5,
        )

        latency = round((time.perf_counter() - t0) * 1000, 1)
        logger.info(f"[soil-rec:{request_id}] done in {latency}ms — top={ranked[0]['crop'] if ranked else 'none'}")

        return {"suitable_crops": ranked}

    except Exception as exc:
        logger.error(f"[soil-rec:{request_id}] ERROR: {exc}")
        logger.error(traceback.format_exc())
        return JSONResponse(status_code=500, content={"status": "error", "detail": str(exc)})
