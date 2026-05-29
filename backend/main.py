"""
SmartCropX Backend API
Main FastAPI application
"""
from fastapi import FastAPI, File, UploadFile, Depends
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
import sys
import traceback
import logging

# ── Environment loading ─────────────────────────────────────────────
try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
except ImportError:
    pass  # python-dotenv is optional; env vars can be set externally

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# Add scripts directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'scripts'))

# Add backend directory itself so community package resolves
sys.path.insert(0, os.path.dirname(__file__))

# ── Community module ────────────────────────────────────────────────
from routers.community import router as community_router, auth_router, seed_if_empty
from db import SessionLocal, engine as _db_engine, Base as _db_base
from community.auth import require_role
from community.models import User as _UserModel

# ── Recommendation module ───────────────────────────────────────────
from routers.recommendation import router as recommend_router
from recommendation.models import CropRecommendationHistory  # ensure model registered

# ── Pesticide module ────────────────────────────────────────────────
from routers.pesticide import router as pesticide_router

# Global variables for lazy loading
soil_model = None
class_names = None
plantdoc_predict_func = None

app = FastAPI(title="SmartCropX API", version="1.0.0")

# ✅ Lazy loading functions
def load_soil_model():
    """Load soil classifier resources lazily."""
    global soil_model, class_names
    if soil_model is None:
        try:
            from services.image_models import ensure_models_trained, _load_model_pair, SOIL_MODEL_PATH, SOIL_LABELS_PATH
            ensure_models_trained()
            pair = _load_model_pair(SOIL_MODEL_PATH, SOIL_LABELS_PATH)
            soil_model = pair.model
            class_names = pair.labels
            logger.info(f"Loaded soil classifier with classes: {class_names}")
        except Exception as e:
            logger.error(f"Failed to load any soil model: {str(e)}")
            raise e
    
    return soil_model, class_names

def load_plantdoc_predictor():
    """Load plant disease predictor lazily."""
    global plantdoc_predict_func
    if plantdoc_predict_func is None:
        try:
            from services.image_models import ensure_models_trained, predict_plant_image
            ensure_models_trained()
            plantdoc_predict_func = predict_plant_image
            logger.info("Loaded plant disease predictor")
        except Exception as e:
            logger.error(f"Failed to load plant disease predictor: {str(e)}")
            raise e
    
    return plantdoc_predict_func



# ✅ CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://superb-patience-production.up.railway.app",
        "http://localhost:5173",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Include community & auth routers
app.include_router(auth_router)
app.include_router(community_router)

# ✅ Include recommendation router
app.include_router(recommend_router)

# ✅ Include pesticide router
app.include_router(pesticide_router)

# ✅ Mount community uploads (AFTER router registration)
COMMUNITY_UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "community_uploads")
os.makedirs(COMMUNITY_UPLOAD_DIR, exist_ok=True)
app.mount("/community-images", StaticFiles(directory=COMMUNITY_UPLOAD_DIR), name="community-images")

# ✅ Root endpoint
@app.get("/")
def root():
    return {"message": "SmartCropX API is running", "status": "healthy", "version": "1.0.0"}

# ✅ Health check routes
@app.get("/health")
@app.get("/api/health")
def health_check():
    return {"status": "API is running"}

@app.get("/healthz")
def health_check_detailed():
    """Detailed health check with model status"""
    status = {
        "status": "healthy",
        "message": "SmartCropX API is running",
        "version": "1.0.0",
        "models": {
            "soil_model": soil_model is not None,
            "plantdoc_predictor": plantdoc_predict_func is not None,
        },
    }
    return status

@app.get("/api/db/health")
def db_health_check():
    """Check database connectivity and return table stats."""
    try:
        db = SessionLocal()
        from community.models import User, Post, Comment
        user_count = db.query(User).count()
        post_count = db.query(Post).count()
        comment_count = db.query(Comment).count()
        db.close()
        return {
            "status": "healthy",
            "database": "SQLite",
            "tables": {
                "users": user_count,
                "posts": post_count,
                "comments": comment_count,
            },
        }
    except Exception as e:
        logger.error(f"DB health check failed: {e}")
        return {"status": "unhealthy", "error": str(e)}

# ✅ Plant Disease Prediction  (RBAC: FARMER + ADMIN)
@app.post("/predict")
async def predict(file: UploadFile = File(...), _user: _UserModel = Depends(require_role("FARMER", "AGRONOMIST", "ADMIN"))):
    try:
        from services.image_models import predict_plant_bytes
        image_bytes = await file.read()
        result = predict_plant_bytes(image_bytes, filename=file.filename)
        return result
    except Exception as e:
        logger.error(f"Plant disease prediction error: {str(e)}")
        logger.error(traceback.format_exc())
        return {
            "error": f"Plant disease prediction failed: {str(e)}",
            "disease": "Unable to predict",
            "confidence": 0.0,
            "why": "Model inference failed for this image."
        }


# ✅ Weather Forecast (7-day ML prediction)  (RBAC: FARMER + ADMIN)
@app.get("/weather-forecast")
def weather_forecast(_user: _UserModel = Depends(require_role("FARMER", "AGRONOMIST", "ADMIN"))):
    try:
        from predict_weather import get_weather_forecast
        forecast = get_weather_forecast()
        return {"status": "success", "data": forecast}
    except Exception as e:
        logger.error(f"Weather forecast error: {str(e)}")
        logger.error(traceback.format_exc())
        return {"status": "error", "message": str(e), "data": []}

# ✅ Current Weather (live from OpenWeatherMap)  (RBAC: FARMER + ADMIN)
@app.get("/weather-current")
def weather_current(city: str = "Cherrapunji", _user: _UserModel = Depends(require_role("FARMER", "AGRONOMIST", "ADMIN"))):
    try:
        from fetch_weather import get_weather
        data = get_weather(city)
        if data:
            return {"status": "success", "data": data}
        return {"status": "error", "message": "Could not fetch weather data", "data": None}
    except Exception as e:
        logger.error(f"Current weather error: {str(e)}")
        return {"status": "error", "message": str(e), "data": None}

# ✅ Weather Alerts  (RBAC: FARMER + ADMIN)
@app.get("/weather-alerts")
def weather_alerts(_user: _UserModel = Depends(require_role("FARMER", "AGRONOMIST", "ADMIN"))):
    try:
        from weather_alerts import check_weather_alerts
        alerts = check_weather_alerts()
        return {"status": "success", "alerts": alerts}
    except Exception as e:
        logger.error(f"Weather alerts error: {str(e)}")
        return {"status": "success", "alerts": []}

@app.post("/predict-soil")
async def predict_soil(file: UploadFile = File(...), _user: _UserModel = Depends(require_role("FARMER", "AGRONOMIST", "ADMIN"))):
    try:
        from services.image_models import ensure_models_trained, predict_soil_bytes
        ensure_models_trained()

        image_bytes = await file.read()
        result = predict_soil_bytes(image_bytes, filename=file.filename)

        return result

    except Exception as e:
        logger.error(f"Soil prediction error: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail=f"Soil prediction failed: {str(e)}",
        )

# ═══════════════════════════════════════════════════════════════════
# ✅ Explainable AI (XAI) Endpoints
# ═══════════════════════════════════════════════════════════════════

@app.post("/api/disease/explain")
async def explain_disease(file: UploadFile = File(...), _user: _UserModel = Depends(require_role("FARMER", "AGRONOMIST", "ADMIN"))):
    """Return a short plain-language disease explanation text."""
    try:
        from services.image_models import ensure_models_trained
        ensure_models_trained()

        image_bytes = await file.read()
        from services.image_models import predict_plant_bytes
        prediction = predict_plant_bytes(image_bytes, filename=file.filename)

        return {
            "status": "success",
            "explanation": prediction["why"],
            "xai_visual": prediction.get("xai_visual", ""),
        }
    except Exception as e:
        logger.error(f"Disease XAI error: {e}")
        logger.error(traceback.format_exc())
        return {
            "status": "error",
            "error": str(e),
            "explanation": "Explainability service encountered an error. Please try again.",
        }


@app.post("/api/soil/explain")
async def explain_soil_endpoint(file: UploadFile = File(...), _user: _UserModel = Depends(require_role("FARMER", "AGRONOMIST", "ADMIN"))):
    """Return a short plain-language soil explanation text."""
    try:
        from services.image_models import ensure_models_trained
        ensure_models_trained()

        image_bytes = await file.read()
        from services.image_models import predict_soil_bytes
        prediction = predict_soil_bytes(image_bytes, filename=file.filename)

        return {
            "status": "success",
            "explanation": prediction["why"],
            "xai_visual": prediction.get("xai_visual", ""),
        }
    except Exception as e:
        logger.error(f"Soil XAI error: {e}")
        logger.error(traceback.format_exc())
        return {
            "status": "error",
            "error": str(e),
            "explanation": "Explainability service encountered an error.",
        }




# ✅ Print all registered routes on startup
@app.on_event("startup")
async def startup_event():
    logger.info("\n📋 SmartCropX API Starting...")
    logger.info("📋 Registered Routes:")
    for route in app.routes:
        if hasattr(route, 'path'):
            logger.info(f"➡️  {route.path}")
    
    # Try to load models on startup (optional - will load on first use if this fails)
    try:
        logger.info("🔄 Attempting to pre-load models...")
        from services.image_models import ensure_models_trained
        ensure_models_trained()
        
        # Try to load soil model
        try:
            load_soil_model()
            logger.info("✅ Soil model loaded successfully")
        except Exception as e:
            logger.warning(f"⚠️ Could not pre-load soil model: {e}")
        
        # Try to load plant disease predictor
        try:
            load_plantdoc_predictor()
            logger.info("✅ Plant disease predictor loaded successfully")
        except Exception as e:
            logger.warning(f"⚠️ Could not pre-load plant disease predictor: {e}")
        

    except Exception as e:
        logger.warning(f"⚠️ Model pre-loading failed: {e}")
        logger.info("📝 Models will be loaded on first use")
    
    # Create recommendation history table
    try:
        _db_base.metadata.create_all(bind=_db_engine)
        logger.info("✅ DB tables synced (recommendation history)")
    except Exception as e:
        logger.warning(f"⚠️ DB table creation failed: {e}")

    # Seed community DB
    try:
        db = SessionLocal()
        seed_if_empty(db)
        db.close()
        logger.info("✅ Community DB ready")
    except Exception as e:
        logger.warning(f"⚠️ Community seed failed: {e}")

    logger.info("✅ SmartCropX API is ready!")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8001))
    logger.info(f"Starting SmartCropX API on port {port} (real_model mode active)")
    uvicorn.run(app, host="0.0.0.0", port=port)
