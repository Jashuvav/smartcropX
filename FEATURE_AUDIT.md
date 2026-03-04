# SmartCropX — Feature Audit Report

> Generated: 2026-03-04  
> Repo: `Jashuvav/smartcropX` (branch `main`)

---

## A. Feature Inventory

| # | Feature Name | Backend Files | Frontend Files | ML / Data Files | Status | How to Demo | Dependencies |
|---|---|---|---|---|---|---|---|
| 1 | **Plant Disease Detection** | `main.py` → `POST /predict` ; `scripts/predict_plantdoc.py` | `pages/PlantDiseaseDetection.jsx` | `models/plantdoc_optimized_v2.keras`, `plantdoc_best.keras` (5 fallback models) ; `models/plantdoc_class_names.json` | ✅ Implemented | Upload leaf image → `/disease-detection` | TensorFlow 2.15, cv2 |
| 2 | **Soil Type Detection** | `main.py` → `POST /predict-soil` ; `create_fallback_soil_model.py` | `pages/SoilPredictor.jsx` | `models/soil_classifier.keras`, `soil_classifier_fallback.keras`, `class_names.json` ; `Soil/` dataset | ✅ Implemented | Upload soil image → `/SoilPredictor` | TensorFlow 2.15, Pillow |
| 3 | **Explainable AI — Disease Grad-CAM** | `main.py` → `POST /api/disease/explain` ; `scripts/xai_gradcam.py` | `pages/PlantDiseaseDetection.jsx` (XAI panel) | Same plantdoc model | ✅ Implemented | Upload image → click "Explain with Grad-CAM" in disease detection page | TensorFlow, cv2 |
| 4 | **Explainable AI — Soil Grad-CAM + SHAP** | `main.py` → `POST /api/soil/explain` ; `scripts/xai_gradcam.py`, `scripts/xai_shap.py` | `pages/SoilPredictor.jsx` (XAI panel) | Same soil model | ✅ Implemented | Upload soil image → click "Explain" | TensorFlow, cv2 |
| 5 | **Explainable AI — Price SHAP** | `main.py` → `GET /api/price/explain/{crop}`, `GET /api/price/explain` ; `scripts/xai_shap.py` | `pages/MarketPrediction.jsx` (XAI section) | XGBoost crop .pkl models | ✅ Implemented | Visit Market Prediction → "Explain" per crop | joblib, xgboost |
| 6 | **XAI Chatbot** | `main.py` → `POST /api/chat`, `GET /api/chat/health` ; `chatbot.py` | `components/XAIChatbot.jsx` (floating bubble) | None (rule-based) | ✅ Implemented | Click chatbot bubble on any page → ask questions | None |
| 7 | **Market Price Prediction** | `main.py` → `GET /market-predictions` ; `scripts/predict_with_graph.py` | `pages/MarketPrediction.jsx` | `models/{banana,onion,tomato,wheat,carrot}_model.pkl` ; `processed_data/*.csv` | ✅ Implemented | Navigate to Market Prediction page | XGBoost, joblib, matplotlib |
| 8 | **Weather Forecast (ML)** | `main.py` → `GET /weather-forecast` ; `scripts/predict_weather.py` | `pages/WeatherForecast.jsx` | `models/weather_forecast.pkl` ; `data/historical_weather.csv` | ✅ Implemented | Navigate to Weather page | joblib |
| 9 | **Current Weather (API)** | `main.py` → `GET /weather-current` ; `scripts/fetch_weather.py` | `pages/WeatherForecast.jsx` | None | ✅ Implemented (hardcoded API key) | Weather page → current section | OpenWeatherMap API key |
| 10 | **Weather Alerts** | `main.py` → `GET /weather-alerts` ; `scripts/weather_alerts.py` | `pages/WeatherForecast.jsx` | None | ✅ Implemented | Weather page → alerts section | OpenWeatherMap API key |
| 11 | **Community Forum — Auth** | `community/auth.py`, `community/routes.py` → `POST /api/auth/register`, `POST /api/auth/login`, `GET /api/auth/me` ; `community/models.py` (User, Role enum) | `pages/LoginPage.jsx`, `pages/RegisterPage.jsx`, `context/AuthContext.js` | None | ✅ Implemented | `/LoginPage`, `/RegisterPage` | SQLAlchemy, python-jose, passlib |
| 12 | **Community Forum — Posts** | `community/routes.py` → CRUD `/api/community/posts`, comments, likes, upload | `pages/CommunityFeed.jsx`, `pages/CreatePost.jsx`, `pages/PostDetail.jsx` | None | ✅ Implemented | `/community` → create, like, comment | SQLAlchemy |
| 13 | **Crop Recommendation (Location + Weather + NDVI)** | `recommendation/routes.py` → `POST /api/recommend/crop`, `GET /api/recommend/health` ; `recommendation/engine.py`, `recommendation/data_sources.py`, `recommendation/schemas.py`, `recommendation/models.py` | `pages/CropRecommendation.jsx` | None (rule-based, Open-Meteo API) | ✅ Implemented | `/crop-recommendation` → fill form → Get Recommendations | httpx |
| 14 | **Soil-Based Crop Suitability** | `recommendation/routes.py` → `POST /api/recommend/soil` ; `recommendation/engine.py` | `pages/SoilRecommendation.jsx` | None (rule-based) | ✅ Implemented | `/soil-recommendation` → fill form → Analyse Soil | None |
| 15 | **Blockchain — Storage Management** | `blockchain/StorageManagement.sol` | `components/StorageForm.js`, `components/web3.js` ; `contracts/StorageManagement.sol` | None | ⚠️ Partial | `/StorageForm` — requires Ganache running on port 7545 + deployed contract | Ganache, Truffle, Web3, MetaMask |
| 16 | **Blockchain — Marketplace** | `blockchain/Marketplace.sol` | `components/Marketplace.js`, `components/marketplaceWeb3.js` ; `contracts/Marketplace.sol` | None | ⚠️ Partial | `/Marketplace` — requires Ganache + deployed contract | Ganache, Truffle, Web3, MetaMask |
| 17 | **Pesticide Recommendation** | `pesticide/knowledge_base.py`, `pesticide/routes.py` → `POST /api/pesticide/recommend`, `GET /api/pesticide/diseases`, `GET /api/pesticide/crops` | `pages/PesticideRecommendation.jsx` | None (rule-based KB) | ✅ Implemented | `/pesticide-recommendation` → enter disease + crop → Get Recommendation | None |
| 18 | **Role-Based Access Control (RBAC)** | `community/auth.py` → `require_role()` dependency ; JWT role claim ; role guards on `/predict`, `/predict-soil`, `/market-predictions`, `/weather-*`, XAI endpoints (FARMER+ADMIN) ; `/api/marketplace/access` (BUYER+ADMIN) ; community delete (ADMIN) | `components/ProtectedRoute.jsx` ; `context/AuthContext.js` (role helpers) ; `pages/Header.jsx` (role badge) | None | ✅ Implemented | Register as different roles → verify route access + role badge in navbar | — |

### Summary of inventory

| Status | Count | Features |
|---|---|---|
| ✅ Implemented | 16 | Disease Detection, Soil Detection, XAI (×3), XAI Chatbot, Market Price, Weather (×3), Auth, Community, Crop Recommendation, Soil Recommendation, Pesticide Recommendation, RBAC |
| ⚠️ Partial | 2 | Blockchain Storage, Blockchain Marketplace |
| ❌ Missing | 0 | — |

---

## B. SRS Feature Compliance Matrix

| SRS Feature | Implemented? | What Works Right Now | What Is Missing | What Must Be Updated | Priority |
|---|---|---|---|---|---|
| **1. Role-Based Access Control (RBAC)** | **Yes** | • 3 roles defined: FARMER, BUYER, ADMIN<br>• Registration accepts role parameter<br>• JWT token includes role claim<br>• `require_role()` FastAPI dependency enforces roles server-side<br>• Prediction endpoints (disease, soil, price, weather, XAI) → FARMER + ADMIN<br>• Marketplace access → BUYER + ADMIN<br>• Community post/comment delete → owner or ADMIN<br>• Frontend `ProtectedRoute` component gates UI by role<br>• Role badge displayed in navbar | • (Fully functional) | • Consider adding admin dashboard for user management | **Done** |
| **2. Explainable AI (XAI)** | **Yes** | • Grad-CAM heatmaps for disease & soil images<br>• SHAP feature importance for price prediction (all 5 crops)<br>• Rule-based fallback when SHAP fails<br>• XAI chatbot explains Grad-CAM & SHAP concepts<br>• Frontend panels show heatmap overlay + feature bars | • (Fully functional) | • Minor: chatbot could link to XAI results contextually | **Low** |
| **3. Community & Advisory System** | **Yes** | • User registration + login (JWT)<br>• Create, read, update, delete posts<br>• Comments on posts<br>• Like / unlike posts<br>• Image upload for posts<br>• Search, tag filter, sort (latest / top)<br>• Seed data on first launch | • Bookmarks model exists but no endpoint<br>• No "advisory" role — experts aren't differentiated | • Add bookmark endpoints<br>• Consider "EXPERT" advisory role | **Low** |
| **4. Soil Type Detection** | **Yes** | • CNN model (`soil_classifier.keras`) classifies uploaded soil images into 4 types: Alluvial, Black, Clay, Red<br>• Returns prediction, confidence, recommended crops, care tips<br>• Fallback model + color-based heuristic fallback<br>• XAI Grad-CAM overlay for explainability | • Only 4 soil classes (Laterite, Sandy, Loamy mentioned elsewhere but not in classifier) | • Consider retraining with more soil types if dataset available | **Low** |
| **5. Crop Recommendation** | **Yes** | • `POST /api/recommend/crop` — accepts lat/lon, soil, pH, NPK<br>• Fetches live weather from Open-Meteo (free, no API key)<br>• Simulates satellite NDVI from coordinates<br>• Rule-based scoring engine with 16 crops<br>• Returns top 3 crops with score + reasons<br>• `POST /api/recommend/soil` — soil-only ranking, top 5<br>• Recommendation history saved to DB<br>• Full frontend pages: `/crop-recommendation`, `/soil-recommendation` | • (Fully functional) | • Could add ML-based scoring in the future | **Low** |
| **6. Plant Disease Detection** | **Yes** | • CNN model (`plantdoc_optimized_v2.keras`) classifies 27 disease/healthy classes<br>• Camera capture + file upload<br>• Returns prediction, confidence, health status, recommendations<br>• XAI Grad-CAM heatmap for explainability | • (Fully functional) | • None critical | **Low** |
| **7. Pesticide Recommendation** | **Yes** | • `POST /api/pesticide/recommend` — accepts disease + optional crop<br>• Knowledge base covers 20+ diseases across 5 crops (Tomato, Rice, Wheat, Cotton, Potato)<br>• Returns pesticide name, dosage, application instructions<br>• Fuzzy disease matching + crop-specific variants<br>• Frontend page at `/pesticide-recommendation` with disease autocomplete + crop dropdown<br>• Linked from Disease Detection page | • (Fully functional) | • Could add more crops/diseases to KB over time | **Done** |

### Compliance Summary

| Status | Count | SRS Items |
|---|---|---|
| ✅ Fully Compliant | 7 | RBAC, XAI, Community, Soil Detection, Crop Recommendation, Disease Detection, Pesticide Recommendation |
| ⚠️ Partially Compliant | 0 | — |
| ❌ Not Implemented | 0 | — |

---

## C. Scope Mismatch / Remove List

Features in the repository that are **not required by the SRS**:

| # | Feature | Classification | Reasoning |
|---|---|---|---|
| 1 | **Weather Forecast (ML + current + alerts)** | 🟡 Keep as "Optional Enhancement" | Useful for farmers; supports crop recommendation context. Works without user action. Not breaking anything. |
| 2 | **Market Price Prediction** | 🟡 Keep as "Optional Enhancement" | Core value-add for farmers; already has XAI SHAP integration. Fully functional. |
| 3 | **XAI Chatbot** | 🟡 Keep as "Optional Enhancement" | Enhances XAI story — explains Grad-CAM, SHAP, crop advice. Rule-based, no API key needed. |
| 4 | **Blockchain — Storage Management** | 🔴 Scope Mismatch → Move to "Future Scope" | SRS does not require blockchain. Requires Ganache + Truffle setup. Fails if Ganache not running. Will confuse reviewers. Abstract mentions it but SRS does not. |
| 5 | **Blockchain — Marketplace** | 🔴 Scope Mismatch → Move to "Future Scope" | Same as above. Requires local Ganache blockchain. Not testable without setup. |
| 6 | **API Test Page** | 🟡 Keep as dev utility | `ApiTestPage.jsx` — useful for developers but should not be in production nav. |

### Recommended Actions

| Feature | Action | Reason |
|---|---|---|
| Weather module | **Keep** | Enhances farmer experience; no harm |
| Market Prediction | **Keep** | Valuable; XAI integrated |
| Chatbot | **Keep** | Supports XAI narrative |
| Blockchain (both) | **Move to Future Scope** | Not in SRS, requires Ganache, breaks without it. Label clearly in README as "Future Scope — requires Ganache" |
| API Test page | **Keep** (hide from nav) | Dev utility |

---

## D. Final Counts

| Metric | Count |
|---|---|
| **Total SRS features fully implemented** | 7 |
| **Total SRS features partially implemented** | 0 |
| **Total SRS features missing** | 0 |
| **Total features to update/fix** | 0 |
| **Total non-SRS features (keep as optional)** | 4 (Weather, Market, Chatbot, API Test) |
| **Total non-SRS features to move to future scope** | 2 (Blockchain Storage, Blockchain Marketplace) |
| — | — |
| **Grand total features in repo** | 18 |
| **Grand total fully working** | 16 |
| **Grand total partially working / broken** | 2 (Blockchain ×2) |
| **Grand total missing to add** | 0 |

---

## E. Backend API Route Map (complete)

| Method | Endpoint | Module | Auth Required |
|---|---|---|---|
| GET | `/` | Health | No |
| GET | `/health`, `/api/health` | Health | No |
| GET | `/healthz` | Health (detailed) | No |
| GET | `/api/chat/health` | Chatbot health | No |
| POST | `/predict` | Plant Disease | Yes (FARMER/ADMIN) |
| POST | `/predict-soil` | Soil Type | Yes (FARMER/ADMIN) |
| GET | `/market-predictions` | Price Prediction | Yes (FARMER/ADMIN) |
| GET | `/weather-forecast` | Weather (ML) | Yes (FARMER/ADMIN) |
| GET | `/weather-current` | Weather (API) | Yes (FARMER/ADMIN) |
| GET | `/weather-alerts` | Weather Alerts | Yes (FARMER/ADMIN) |
| POST | `/api/disease/explain` | XAI Grad-CAM | Yes (FARMER/ADMIN) |
| POST | `/api/soil/explain` | XAI Grad-CAM + SHAP | Yes (FARMER/ADMIN) |
| GET | `/api/price/explain/{crop}` | XAI SHAP | Yes (FARMER/ADMIN) |
| GET | `/api/price/explain` | XAI SHAP (all) | Yes (FARMER/ADMIN) |
| POST | `/api/chat` | Chatbot | No |
| POST | `/api/auth/register` | Auth | No |
| POST | `/api/auth/login` | Auth | No |
| GET | `/api/auth/me` | Auth | Yes (JWT) |
| GET | `/api/community/posts` | Community | Optional |
| POST | `/api/community/posts` | Community | Yes |
| GET | `/api/community/posts/{id}` | Community | Optional |
| PUT | `/api/community/posts/{id}` | Community | Yes (owner) |
| DELETE | `/api/community/posts/{id}` | Community | Yes (owner) |
| POST | `/api/community/posts/{id}/comments` | Community | Yes |
| GET | `/api/community/posts/{id}/comments` | Community | Optional |
| DELETE | `/api/community/comments/{id}` | Community | Yes (owner) |
| POST | `/api/community/posts/{id}/like` | Community | Yes |
| GET | `/api/community/posts/{id}/likes` | Community | Optional |
| POST | `/api/community/upload` | Community (image) | Yes |
| GET | `/api/recommend/health` | Recommendation | No |
| POST | `/api/recommend/crop` | Crop Recommendation | No |
| POST | `/api/recommend/soil` | Soil Recommendation | No |
| GET | `/api/marketplace/access` | Marketplace RBAC | Yes (BUYER/ADMIN) |
| POST | `/api/pesticide/recommend` | Pesticide Recommendation | No |
| GET | `/api/pesticide/diseases` | Pesticide (list diseases) | No |
| GET | `/api/pesticide/crops` | Pesticide (list crops) | No |
| GET | `/api/pesticide/health` | Pesticide health | No |

## F. Frontend Route Map (complete)

| Path | Component | Nav Link | Role Guard |
|---|---|---|---|
| `/` | Home (Hero + Dashboard + News + Contact) | "Home" | — |
| `/disease-detection` | PlantDiseaseDetection | (from dashboard cards) | FARMER/ADMIN |
| `/market-prediction` | MarketPrediction | (from dashboard cards) | FARMER/ADMIN |
| `/weather-prediction` | WeatherForecast | (from dashboard cards) | FARMER/ADMIN |
| `/SoilPredictor` | SoilPredictor | (from dashboard cards) | FARMER/ADMIN |
| `/crop-recommendation` | CropRecommendation | "Recommend" nav item | — |
| `/soil-recommendation` | SoilRecommendation | (linked from crop-recommendation) | — |
| `/pesticide-recommendation` | PesticideRecommendation | "Pesticide" nav item | — |
| `/community` | CommunityFeed | "Community" nav item | — |
| `/community/new` | CreatePost | (button in CommunityFeed) |
| `/community/post/:id` | PostDetail | (click post in feed) |
| `/LoginPage` | LoginPage | (login button in header) |
| `/RegisterPage` | RegisterPage | (link from login) |
| `/StorageForm` | StorageForm (blockchain) | (from dashboard cards) |
| `/Marketplace` | Marketplace (blockchain) | (from dashboard cards) |
| `/api-test` | ApiTestPage | (hidden / dev) |

## G. ML Model Inventory

| File | Type | Used By | Size Concern |
|---|---|---|---|
| `plantdoc_optimized_v2.keras` | TF/Keras CNN | Disease Detection | ~50 MB (Git LFS) |
| `plantdoc_optimized_ema.keras` | TF/Keras CNN | Disease Detection (fallback) | ~50 MB (Git LFS) |
| `plantdoc_optimized.keras` | TF/Keras CNN | Disease Detection (fallback) | ~50 MB (Git LFS) |
| `plantdoc_best.keras` | TF/Keras CNN | Disease Detection (fallback) | ~50 MB (Git LFS) |
| `best_plantdoc_model.keras` | TF/Keras CNN | Disease Detection (fallback) | ~50 MB (Git LFS) |
| `soil_classifier.keras` | TF/Keras CNN | Soil Type Detection | ~10 MB (Git LFS) |
| `soil_classifier_fallback.keras` | TF/Keras CNN | Soil Type (fallback) | ~2 MB (Git LFS) |
| `banana_model.pkl` | XGBoost | Price Prediction | ~1 MB |
| `onion_model.pkl` | XGBoost | Price Prediction | ~1 MB |
| `tomato_model.pkl` | XGBoost | Price Prediction | ~1 MB |
| `wheat_model.pkl` | XGBoost | Price Prediction | ~1 MB |
| `carrot_model.pkl` | XGBoost | Price Prediction | ~1 MB |
| `crop_demand_model.pkl` | XGBoost | (unused / legacy) | ~1 MB |
| `weather_forecast.pkl` | Scikit-learn | Weather ML Prediction | ~1 MB |
| `class_names.json` | JSON | Soil class labels | <1 KB |
| `plantdoc_class_names.json` | JSON | Disease class labels | <1 KB |
