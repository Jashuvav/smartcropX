"""
SmartCropX — Recommendation history model (SQLAlchemy).
"""

import uuid
import datetime
from sqlalchemy import Column, String, Text, Float, DateTime, JSON
from community.database import Base


def _uuid() -> str:
    return uuid.uuid4().hex


def _now():
    return datetime.datetime.utcnow()


class CropRecommendationHistory(Base):
    __tablename__ = "crop_recommendation_history"

    id = Column(String(32), primary_key=True, default=_uuid)
    user_id = Column(String(32), nullable=True, index=True)  # nullable for anonymous
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    district = Column(String(200), nullable=True)
    soil_type = Column(String(60), nullable=False)
    ph = Column(Float, nullable=True)
    nitrogen = Column(Float, nullable=True)
    phosphorus = Column(Float, nullable=True)
    potassium = Column(Float, nullable=True)
    recommended_crops = Column(JSON, nullable=True)
    weather_summary = Column(JSON, nullable=True)
    ndvi = Column(Float, nullable=True)
    created_at = Column(DateTime, default=_now)
