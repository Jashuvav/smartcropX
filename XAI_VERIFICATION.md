# Explainable AI (XAI) — Verification Guide

SmartCropX now includes **Explainable AI** across all three modules:

| Module | Technique | Endpoint | What it returns |
|--------|-----------|----------|-----------------|
| Plant Disease Detection | **Grad-CAM** | `POST /api/disease/explain` | Heatmap, overlay image, top-3 activation regions |
| Soil Classification | **Grad-CAM + Domain Rules** | `POST /api/soil/explain` | Heatmap, overlay, 5 visual-feature explanations |
| Market Price Prediction | **SHAP TreeExplainer** | `GET /api/price/explain/{crop}` | Top-5 features with impact values & directions |
| Market Price (all crops) | **SHAP TreeExplainer** | `GET /api/price/explain` | SHAP for all 5 crops in one call |

---

## Quick Start

```bash
# 1. Start backend (port 8001)
cd SmartCropX
$env:TF_ENABLE_ONEDNN_OPTS = "0"
.\.venv\Scripts\python.exe -m uvicorn backend.main:app --host 0.0.0.0 --port 8001

# 2. Start frontend (port 3000) — in another terminal
cd SmartCropX/frontend
$env:BROWSER = "none"
npm start

# 3. Open http://localhost:3000
```

> **Note:** The frontend `api.js` currently points to `localhost:8001`. If you change the
> backend port, update `DEVELOPMENT_URL` in `frontend/src/config/api.js`.

---

## Backend Endpoint Verification

### 1. Disease Grad-CAM

```powershell
# PowerShell — using Python requests
.\.venv\Scripts\python.exe -c @"
import requests, os, glob
imgs = glob.glob('backend/PlantDoc-Dataset/test/**/*.*', recursive=True)
with open(imgs[0], 'rb') as f:
    r = requests.post('http://localhost:8001/api/disease/explain',
                      files={'file': (os.path.basename(imgs[0]), f, 'image/jpeg')},
                      timeout=120)
d = r.json()
print('Method :', d['method'])
print('Heatmap:', len(d['heatmap']), 'chars')
print('Overlay:', len(d['overlay']), 'chars')
print('Regions:', d['regions'])
print('Predict:', d['prediction'])
"@
```

**Expected output:**
```
Method : grad-cam
Heatmap: ~370000 chars (base64 PNG)
Overlay: ~20000000 chars (base64 PNG, depends on image size)
Regions: [{'x': ..., 'y': ..., 'intensity': 0.8+, 'size': ...}]
Predict: {'class': 'Apple leaf', 'confidence': 0.50, 'status': 'HEALTHY'}
```

### 2. Soil Grad-CAM + Features

```powershell
.\.venv\Scripts\python.exe -c @"
import requests, os, glob
imgs = glob.glob('backend/Soil/test/**/*.*', recursive=True)
with open(imgs[0], 'rb') as f:
    r = requests.post('http://localhost:8001/api/soil/explain',
                      files={'file': (os.path.basename(imgs[0]), f, 'image/jpeg')},
                      timeout=120)
d = r.json()
print('Method :', d['method'])
print('Heatmap:', len(d['heatmap']), 'chars')
print('Predict:', d['prediction'])
print('Features:', d['feature_explanation']['method'],
      len(d['feature_explanation']['features']), 'features')
"@
```

**Expected output:**
```
Method : grad-cam
Heatmap: ~11000 chars
Predict: {'prediction': 'Clay soil', 'confidence': 87.7}
Features: domain-rule-based 5 features
```

### 3. Price SHAP (single crop)

```powershell
Invoke-WebRequest -Uri "http://localhost:8001/api/price/explain/banana" -UseBasicParsing |
  Select-Object -ExpandProperty Content | ConvertFrom-Json | Format-List
```

**Expected fields:**
```
status  : success
crop    : banana
method  : shap-tree-explainer
features: [{feature: "Min Price (Rs./Quintal)", impact: 44.48, direction: "negative", ...}, ...]
```

### 4. Price SHAP (all crops)

```powershell
Invoke-WebRequest -Uri "http://localhost:8001/api/price/explain" -UseBasicParsing |
  Select-Object -ExpandProperty Content | ConvertFrom-Json |
  Select-Object -ExpandProperty data
```

Returns `{ banana: {...}, onion: {...}, tomato: {...}, wheat: {...}, carrot: {...} }`.

---

## Frontend Verification

1. **Plant Disease Detection** page → Upload an image → Click **"Detect Disease"** →
   After results, click **"🔍 Why this prediction? (XAI)"** → See Grad-CAM heatmap & overlay.

2. **Market Predictions** page → Expand any crop card → Click **"Explain"** (beaker icon) →
   See SHAP feature importance bars with ↑/↓ direction labels.

3. **Soil Predictor** page → Upload a soil image → Click **"Analyse Soil"** →
   After results, click **"🔍 Why this soil type? (Explainable AI)"** → See heatmap + feature bars.

---

## Architecture

```
backend/scripts/
  xai_gradcam.py    ← Grad-CAM engine (real + mock fallback)
  xai_shap.py       ← SHAP TreeExplainer + rule-based soil features

backend/main.py     ← 4 new endpoints under # XAI Endpoints section

frontend/src/config/api.js                ← 4 new endpoint constants
frontend/src/pages/PlantDiseaseDetection.jsx  ← XAI panel
frontend/src/pages/MarketPrediction.jsx       ← SHAP panel in expanded card
frontend/src/pages/SoilPredictor.jsx          ← XAI panel (Grad-CAM + features)
```

### Fallback Behaviour

| Scenario | Fallback |
|----------|----------|
| Model file missing | Mock Gaussian heatmap (`method: "mock-gradcam"`) |
| Grad-CAM computation error | Mock Gaussian heatmap |
| SHAP computation error | Curated rule-based feature ranking (`method: "rule-based"`) |
| Soil features | Always domain-rule-based (CNN has no tabular features) |

### Dependencies Added

- `shap >= 0.46` — SHAP TreeExplainer for XGBoost models
- `scipy` — Region detection via `ndimage.label`
- `opencv-python` — Colormap computation for Grad-CAM
- All were already available or installed in the venv.
