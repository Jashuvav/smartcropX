"""
SmartCropX — Pydantic schemas for the recommendation module.
"""

from typing import Optional, List
from pydantic import BaseModel, Field


class CropRecommendInput(BaseModel):
    latitude: float = Field(..., ge=-90, le=90, description="Latitude")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude")
    district: Optional[str] = Field(None, max_length=200, description="District / locality name")
    soil_type: str = Field(..., min_length=1, max_length=60, description="Soil type (alluvial, black, red, laterite, sandy, clay, loamy)")
    ph: float = Field(..., ge=0, le=14, description="Soil pH value")
    nitrogen: float = Field(..., ge=0, description="Nitrogen content (kg/ha)")
    phosphorus: float = Field(..., ge=0, description="Phosphorus content (kg/ha)")
    potassium: float = Field(..., ge=0, description="Potassium content (kg/ha)")


class SoilRecommendInput(BaseModel):
    soil_type: str = Field(..., min_length=1, max_length=60)
    ph: float = Field(..., ge=0, le=14)
    nitrogen: float = Field(..., ge=0)
    phosphorus: float = Field(..., ge=0)
    potassium: float = Field(..., ge=0)


class CropResult(BaseModel):
    crop: str
    score: float
    reason: str


class SoilCropResult(BaseModel):
    crop: str
    suitability: float


class CropRecommendResponse(BaseModel):
    recommended_crops: List[CropResult]
    weather_summary: dict
    ndvi: float


class SoilRecommendResponse(BaseModel):
    suitable_crops: List[SoilCropResult]
