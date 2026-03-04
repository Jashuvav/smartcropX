# SmartCropX — Review / Demo Walkthrough

> For reviewers, examiners, and demo audiences.  
> Generated: 2026-03-04

---

## Prerequisites

| Item | Command / URL |
|---|---|
| Python 3.10+ | `python --version` |
| Node.js 18+ | `node --version` |
| Backend venv | `cd backend && python -m venv .venv && .venv\Scripts\activate && pip install -r requirements.txt` |
| Frontend deps | `cd frontend && npm install` |

### Start Servers

```bash
# Terminal 1 — Backend (port 8001)
cd backend
.venv\Scripts\activate
uvicorn main:app --host 0.0.0.0 --port 8001 --reload

# Terminal 2 — Frontend (port 3000)
cd frontend
npm start
```

Open **http://localhost:3000** in a browser.

---

## Module-by-Module Demo Steps

### 1. Plant Disease Detection (SRS ✅)

| Route | `/disease-detection` |
|---|---|
| Backend | `POST /api/predict/disease` + `POST /api/disease/explain` |

**Steps:**
1. Navigate to **Disease Detection** from the navbar.
2. Click **Upload Image** and select any leaf image (e.g., a tomato leaf with spots).
   - Alternatively, click the **Camera** icon to capture a photo.
3. Click **Detect Disease**.
4. Observe: disease name, confidence %, description card.
5. Click the **"Explain with XAI"** button.
6. Observe: Grad-CAM heatmap overlaid on the uploaded image.

**curl test:**
```bash
curl -X POST http://localhost:8001/api/predict/disease \
  -F "file=@test_leaf.jpg"
```

---

### 2. Soil Detection (SRS ✅)

| Route | `/SoilPredictor` |
|---|---|
| Backend | `POST /api/predict/soil` + `POST /api/soil/explain` |

**Steps:**
1. Navigate to **Soil Detection** from the navbar.
2. Upload a soil image.
3. Click **Predict Soil Type**.
4. Observe: soil type, confidence %, properties card.
5. Click **"Explain with XAI"** to see Grad-CAM heatmap.

**curl test:**
```bash
curl -X POST http://localhost:8001/api/predict/soil \
  -F "file=@soil_sample.jpg"
```

---

### 3. XAI — Explainable AI (SRS ✅)

XAI is integrated into three modules. Demonstrate each:

| Module | XAI Method | Endpoint |
|---|---|---|
| Disease Detection | Grad-CAM | `POST /api/disease/explain` |
| Soil Detection | Grad-CAM | `POST /api/soil/explain` |
| Market Prediction | SHAP | `POST /api/price/explain/{crop}` |

**Steps (already covered above for disease/soil):**
- For Market Prediction XAI, see step 4 below.

---

### 4. Market Price Prediction (Optional Enhancement, not SRS-required)

| Route | `/market-prediction` |
|---|---|
| Backend | `POST /api/predict/price/{crop}` + `POST /api/price/explain/{crop}` |

**Steps:**
1. Navigate to **Market Prediction**.
2. Select a crop from the 5 available: Banana, Onion, Tomato, Wheat, Carrot.
3. Observe: 30-day price forecast chart + current price card.
4. Click **"Explain Prediction"** button.
5. Observe: SHAP feature importance bar chart showing which factors drive the price.

**curl test:**
```bash
curl -X POST http://localhost:8001/api/predict/price/tomato
curl -X POST http://localhost:8001/api/price/explain/tomato
```

---

### 5. Weather Forecast (Optional Enhancement)

| Route | `/weather-prediction` |
|---|---|
| Backend | `GET /api/weather/current` + `GET /api/weather/forecast` + `GET /api/weather/alerts` |

**Steps:**
1. Navigate to **Weather Forecast**.
2. Observe: current weather card with temperature, humidity, wind.
3. Scroll to see the 7-day forecast cards.
4. Check the weather alerts section (displays active advisories if any).

**curl test:**
```bash
curl http://localhost:8001/api/weather/current
curl http://localhost:8001/api/weather/forecast
```

---

### 6. Community Forum (SRS ✅)

| Route | `/community`, `/community/new`, `/community/post/:id` |
|---|---|
| Backend | `POST /api/auth/register`, `POST /api/auth/login`, CRUD at `/api/community/posts` |

**Steps:**
1. Click **Register** → create an account (username, email, password).
2. Click **Login** → enter credentials.
3. Navigate to **Community**.
4. Observe: feed of posts (seeded automatically on first boot).
5. Click **Create Post** → fill in title, content, optional image → submit.
6. Click on a post → see full detail view with comments.
7. Add a comment.
8. Click the ❤️ like button.
9. Verify the like count increments.

**curl test:**
```bash
# Register
curl -X POST http://localhost:8001/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"reviewer","email":"rev@test.com","password":"Pass123!"}'

# Login
curl -X POST http://localhost:8001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"rev@test.com","password":"Pass123!"}'
# → returns { "access_token": "eyJ..." }
```

---

### 7. Crop Recommendation (SRS ✅)

| Route | `/crop-recommendation` |
|---|---|
| Backend | `POST /api/recommend/crop` |

**Steps:**
1. Navigate to **Crop Recommendation**.
2. The form auto-detects your location (or enter manually: latitude/longitude).
3. Observe: Weather card and NDVI card auto-populate.
4. Adjust optional parameters (soil type, area, budget) if desired.
5. Click **Get Recommendations**.
6. Observe: top 3 recommended crops with suitability score, expected yield, growing tips.

**curl test:**
```bash
curl -X POST http://localhost:8001/api/recommend/crop \
  -H "Content-Type: application/json" \
  -d '{"latitude":17.385,"longitude":78.4867,"soil_type":"Black","area_hectares":2,"budget_inr":50000}'
```

---

### 8. Soil-Based Recommendation (SRS ✅)

| Route | `/soil-recommendation` |
|---|---|
| Backend | `POST /api/recommend/soil` |

**Steps:**
1. Navigate to **Soil Recommendation**.
2. Enter soil parameters: N, P, K, pH, moisture.
3. Click **Get Recommendations**.
4. Observe: top 5 crops suited to those soil conditions.

**curl test:**
```bash
curl -X POST http://localhost:8001/api/recommend/soil \
  -H "Content-Type: application/json" \
  -d '{"nitrogen":80,"phosphorus":40,"potassium":50,"ph":6.5,"moisture":60}'
```

---

### 9. XAI Chatbot (Optional Enhancement)

| Component | Floating bubble, bottom-right on every page |
|---|---|
| Backend | `POST /api/chat` |

**Steps:**
1. Click the 💬 chat bubble in the bottom-right corner (visible on any page).
2. Type a question: "What is crop rotation?"
3. Observe: rule-based answer from the agricultural knowledge base.
4. Try: "How to prevent tomato blight?"
5. Try: "What soil is best for wheat?"

---

### 10. RBAC — Role-Based Access (SRS — ⚠️ PARTIAL)

**Current state:** Roles (FARMER, BUYER, ADMIN) are stored in the database and JWT token but NOT enforced. Any logged-in user can perform any action.

**What to demonstrate:**
- Show the role field in the JWT payload (decode at jwt.io).
- Show the `Role` enum in the codebase.
- Acknowledge the gap: enforcement is on the roadmap (see ROADMAP.md, Task U-1).

---

### 11. Pesticide Recommendation (SRS — ❌ MISSING)

**Current state:** Not implemented. Zero backend endpoints, zero frontend pages.

**What to say during demo:**
- "This module is identified as a gap and is the top priority on our roadmap (see ROADMAP.md, Task A-1)."

---

## Blockchain Features (Future Scope — Not SRS)

### Storage Management

| Route | `/StorageForm` |
|---|---|
| Requires | Ganache running on port 7545 + MetaMask |

> ⚠️ Only demo if Ganache + Truffle environment is available.

### Marketplace

| Route | `/Marketplace` |
|---|---|
| Requires | Ganache running on port 7545 + MetaMask |

> ⚠️ Only demo if Ganache + Truffle environment is available.

---

## Quick Health Checks

```bash
# Backend health
curl http://localhost:8001/

# API docs
open http://localhost:8001/docs

# Recommendation health
curl http://localhost:8001/api/recommend/health

# Frontend
open http://localhost:3000
```

---

## Summary Table

| # | Feature | SRS Required | Status | Demo-able |
|---|---|---|---|---|
| 1 | Plant Disease Detection | ✅ | ✅ Complete | ✅ Yes |
| 2 | Soil Detection | ✅ | ✅ Complete | ✅ Yes |
| 3 | XAI (Grad-CAM + SHAP) | ✅ | ✅ Complete | ✅ Yes |
| 4 | Community Forum | ✅ | ✅ Complete | ✅ Yes |
| 5 | Crop Recommendation | ✅ | ✅ Complete | ✅ Yes |
| 6 | Soil Recommendation | ✅ | ✅ Complete | ✅ Yes |
| 7 | RBAC | ✅ | ⚠️ Partial | ⚠️ Show code |
| 8 | Pesticide Recommendation | ✅ | ❌ Missing | ❌ No |
| 9 | Market Prediction | ❌ | ✅ Complete | ✅ Yes |
| 10 | Weather Forecast | ❌ | ✅ Complete | ✅ Yes |
| 11 | XAI Chatbot | ❌ | ✅ Complete | ✅ Yes |
| 12 | Blockchain (×2) | ❌ | ⚠️ Needs Ganache | ⚠️ Conditional |
