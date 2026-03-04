"""
SmartCropX — Pesticide Recommendation API routes.

POST /api/pesticide/recommend  — look up pesticide for a given disease + crop
GET  /api/pesticide/diseases   — list all known diseases
GET  /api/pesticide/crops      — list supported crops
GET  /api/pesticide/health     — module health
"""

import logging
from typing import Optional

from fastapi import APIRouter
from pydantic import BaseModel, Field

from .knowledge_base import lookup_pesticide, PESTICIDE_KB, SUPPORTED_CROPS

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/pesticide", tags=["Pesticide"])


# ── Schemas ─────────────────────────────────────────────────────────

class PesticideInput(BaseModel):
    disease: str = Field(..., min_length=1, max_length=200, description="Detected disease name")
    crop: Optional[str] = Field(None, max_length=100, description="Crop name (optional)")


class PesticideResponse(BaseModel):
    pesticide: str
    dosage: str
    instructions: str
    disease: str
    crop: str
    matched: bool


# ── Endpoints ───────────────────────────────────────────────────────

@router.get("/health")
def pesticide_health():
    return {
        "status": "ok",
        "module": "pesticide-recommendation",
        "diseases_count": len(PESTICIDE_KB),
        "crops": SUPPORTED_CROPS,
    }


@router.post("/recommend", response_model=PesticideResponse)
def recommend_pesticide(payload: PesticideInput):
    """Return a pesticide recommendation for the given disease (+optional crop)."""
    logger.info(f"[pesticide] disease={payload.disease!r} crop={payload.crop!r}")
    result = lookup_pesticide(payload.disease, payload.crop)
    return PesticideResponse(**result)


@router.get("/diseases")
def list_diseases():
    """List all diseases in the knowledge base."""
    return {
        "diseases": sorted(
            [d.title() for d in PESTICIDE_KB.keys() if d != "healthy"]
        )
    }


@router.get("/crops")
def list_crops():
    """List all supported crops."""
    return {"crops": SUPPORTED_CROPS}
