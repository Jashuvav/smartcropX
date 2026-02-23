# SmartCropX - How to Run

## Prerequisites
- **Python 3.13+** with pip
- **Node.js 18+** with npm
- (Optional) **Ganache** on port 7545 for blockchain features

---

## Quick Start

### 1. Backend (Terminal 1)
```bash
cd AgriSync
python -m venv .venv

# Activate venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r backend/requirements.txt
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

### 2. Frontend (Terminal 2)
```bash
cd AgriSync/frontend
npm install
npm start
```

### 3. Open Browser
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Swagger Docs: http://localhost:8000/docs

---

## API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/` | GET | Root - API status |
| `/health` | GET | Health check |
| `/healthz` | GET | Detailed health with model status |
| `/predict` | POST | Plant disease detection (upload image) |
| `/predict-soil` | POST | Soil type classification (upload image) |
| `/market-predictions` | GET | 5-crop price forecasts (banana, onion, tomato, wheat, carrot) |
| `/weather-forecast` | GET | 7-day ML weather forecast |
| `/weather-current` | GET | Live weather from OpenWeatherMap |
| `/weather-alerts` | GET | Weather alert checks |
| `/graphs/{filename}` | GET | Generated prediction graph images |

---

## Feature Status

| Feature | Status | Route |
|---|---|---|
| Plant Disease Detection | Working (Upload + Camera) | `/disease-detection` |
| Soil Type Prediction | Working | `/SoilPredictor` |
| Market Price Prediction | Working (5 crops with graphs) | `/market-prediction` |
| Weather Forecast | Working (API + fallback) | `/weather-prediction` |
| Storage Management | Requires Ganache | `/StorageForm` |
| Marketplace | Requires Ganache | `/Marketplace` |
| Login/Register | UI only (no auth backend) | `/LoginPage`, `/RegisterPage` |

---

## Verification Checklist

1. **Backend Health**: `curl http://localhost:8000/healthz`
   - All 3 models should show `true`

2. **Market Predictions**: `curl http://localhost:8000/market-predictions`
   - Should return 5 crops with category, trend, predictions

3. **Weather Forecast**: `curl http://localhost:8000/weather-forecast`
   - Should return 7 days of forecast data

4. **Frontend**: Open http://localhost:3000
   - Header shows "SmartCropX"
   - Dashboard cards navigate to correct pages
   - Market Prediction shows live data with category filters
   - Weather Forecast shows ML predictions (or graceful fallback)

---

## Configuration Files

- `backend/.env` - Backend config (PORT, API keys, CORS)
- `frontend/.env` - Frontend config (API URL, Ganache URL, contract addresses)
- See `.env.example` files for templates

---

## Tech Stack
- **Backend**: FastAPI + Python 3.13 + TensorFlow 2.20 + XGBoost 3.2 + scikit-learn
- **Frontend**: React 19 + Tailwind CSS 3 + Framer Motion 12 + Axios + Lucide React
- **ML Models**: Keras (soil, plant disease), XGBoost (crop prices), sklearn (weather)
- **Blockchain**: Solidity + Web3.js + Ganache (optional)
