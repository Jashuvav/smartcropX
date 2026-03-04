# 🌿 SmartCropX — AI-Powered Smart Agriculture Platform

**SmartCropX** is a full-stack smart agriculture platform combining **AI/ML**, **Deep Learning**, and **Explainable AI (XAI)** to help farmers make data-driven decisions — from detecting plant diseases to predicting market prices, monitoring weather, analyzing soil, and connecting with the farming community.

🔗 **GitHub**: [https://github.com/Jashuvav/smartcropX](https://github.com/Jashuvav/smartcropX)

---

## 📋 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
- [API Reference](#-api-reference)
- [AI/ML Models](#-aiml-models)
- [Explainable AI (XAI)](#-explainable-ai-xai)
- [Community Forum](#-community-forum)

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🌿 **Plant Disease Detection** | Upload a leaf image → AI identifies the disease using EfficientNetB4 deep learning model |
| 🌱 **Soil Type Detection** | Classify soil type from images using a trained CNN model with care & crop recommendations |
| 🧑‍🌾 **Crop Recommendation** | Get AI-powered crop, soil, and pesticide recommendations based on environmental conditions |
| 🔍 **Explainable AI (XAI)** | Grad-CAM heatmaps and SHAP feature explanations for model transparency |
| 👥 **Community Forum** | Post, comment, like, and share knowledge — with JWT auth and role-based access (Farmer/Buyer/Admin) |
| 🌦️ **Weather Module** | ML-based weather prediction with real-time alerts for extreme conditions |
| 📈 **Market Price Prediction** | Predict future market prices for crops (Tomato, Onion, Wheat, Banana, Carrot) using XGBoost & Random Forest |

---

## 🧰 Tech Stack

| Layer | Technologies |
|-------|-------------|
| **Frontend** | React 19, Tailwind CSS 3, React Router 6, Axios, Framer Motion, Lucide Icons |
| **Backend** | FastAPI, Python 3.13, Uvicorn, Pydantic |
| **AI / ML** | TensorFlow, Keras (EfficientNetB4), Scikit-learn, XGBoost, OpenCV |
| **XAI** | Grad-CAM (tf-keras-vis), SHAP |
| **Auth** | JWT (HS256) via python-jose, passlib + bcrypt |
| **Database** | SQLite + SQLAlchemy 2.0 ORM |
| **Data Tools** | Pandas, NumPy, Matplotlib |

---

## 📁 Project Structure

```
SmartCropX/
├── backend/
│   ├── main.py                  # FastAPI app with all routers
│   ├── community/               # Community forum module
│   │   ├── models.py            # SQLAlchemy models (User, Post, Comment, Like)
│   │   ├── schemas.py           # Pydantic request/response schemas
│   │   ├── auth.py              # JWT authentication & RBAC
│   │   ├── routes.py            # Community & auth API routes
│   │   └── database.py          # SQLite database setup
│   ├── recommendation/          # Crop recommendation module
│   │   ├── routes.py            # Recommendation API routes
│   │   ├── schemas.py           # Input/output schemas
│   │   └── models.py            # Recommendation history model
│   ├── pesticide/               # Pesticide recommendation module
│   │   ├── routes.py            # Pesticide API routes
│   │   └── knowledge_base.py    # Disease-to-pesticide mapping
│   ├── scripts/
│   │   ├── predict_plantdoc.py  # Plant disease prediction
│   │   ├── predict_weather.py   # Weather forecasting
│   │   ├── predict_with_graph.py # Crop price prediction + graph
│   │   ├── xai_gradcam.py       # Grad-CAM explainability
│   │   ├── xai_shap.py          # SHAP explainability
│   │   └── ...training scripts
│   ├── models/                  # Trained .keras model files
│   └── data/                    # CSV datasets + SQLite DB
├── frontend/
│   ├── src/
│   │   ├── App.js               # Routes & AuthProvider
│   │   ├── context/AuthContext.js
│   │   ├── components/
│   │   │   └── ProtectedRoute.jsx  # Role-based route guard
│   │   └── pages/
│   │       ├── Header.jsx           # Navigation bar
│   │       ├── AgriDashboard.jsx    # Main dashboard (5 feature cards)
│   │       ├── PlantDiseaseDetection.jsx
│   │       ├── SoilPredictor.jsx
│   │       ├── MarketPrediction.jsx
│   │       ├── WeatherForecast.jsx
│   │       ├── CropRecommendation.jsx
│   │       ├── PesticideRecommendation.jsx
│   │       ├── CommunityFeed.jsx
│   │       ├── CreatePost.jsx
│   │       ├── PostDetail.jsx
│   │       └── LoginPage.jsx / RegisterPage.jsx
│   └── public/
├── README.md
└── .gitignore
```

---

## 🚀 Getting Started

### Prerequisites
- **Python 3.10+**
- **Node.js 18+** and npm
- **Git**

### 1. Clone the Repository

```bash
git clone https://github.com/Jashuvav/smartcropX.git
cd smartcropX
```

### 2. Backend Setup

```bash
cd backend
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
```

### 3. Start the Backend Server

```bash
uvicorn main:app --host 0.0.0.0 --port 8001
# Server runs at http://localhost:8001
# API docs at http://localhost:8001/docs
```

### 4. Frontend Setup

```bash
cd frontend
npm install
npm start
# App runs at http://localhost:3000
```

---

## 📡 API Reference

Base URL: `http://localhost:8001`

### Core Prediction Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/predict` | FARMER/ADMIN | Plant disease detection (upload image) |
| POST | `/predict-soil` | FARMER/ADMIN | Soil type classification (upload image) |
| GET | `/market-predictions` | FARMER/ADMIN | Crop price predictions with graphs |
| GET | `/weather-forecast` | FARMER/ADMIN | 7-day ML weather forecast |
| GET | `/weather-current?city=` | FARMER/ADMIN | Live weather from OpenWeatherMap |
| GET | `/weather-alerts` | FARMER/ADMIN | Extreme weather alerts |

### Explainable AI Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/api/disease/explain` | FARMER/ADMIN | Grad-CAM heatmap for disease prediction |
| POST | `/api/soil/explain` | FARMER/ADMIN | Grad-CAM heatmap + feature explanation for soil |
| GET | `/api/price/explain/{crop}` | FARMER/ADMIN | SHAP explanation for a crop's price model |
| GET | `/api/price/explain` | FARMER/ADMIN | SHAP explanations for all crops |

### Recommendation Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/api/recommend/crop` | — | Get crop recommendation based on conditions |
| POST | `/api/recommend/soil` | — | Get soil-based recommendation |
| POST | `/api/pesticide/recommend` | — | Get pesticide recommendation for a disease |
| GET | `/api/pesticide/diseases` | — | List supported diseases |
| GET | `/api/pesticide/crops` | — | List supported crops |

### Health Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` or `/api/health` | Basic health check |
| GET | `/healthz` | Detailed health check (model status) |

### Authentication Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/api/auth/register` | — | Create account (name, email, password, role) |
| POST | `/api/auth/login` | — | Returns JWT access token |
| GET | `/api/auth/me` | ✅ | Get current user profile |

### Community Forum Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/api/community/posts` | — | List posts (search, tag, sort) |
| POST | `/api/community/posts` | ✅ | Create a new post |
| GET | `/api/community/posts/{id}` | — | Get post details |
| PATCH | `/api/community/posts/{id}` | ✅ | Edit post (author/admin) |
| DELETE | `/api/community/posts/{id}` | ✅ | Delete post (author/admin) |
| POST | `/api/community/posts/{id}/comments` | ✅ | Add a comment |
| DELETE | `/api/community/comments/{id}` | ✅ | Delete a comment |
| POST | `/api/community/posts/{id}/like` | ✅ | Toggle like on a post |

---

## 🧠 AI/ML Models

### Plant Disease Detection
- **Architecture**: EfficientNetB4 (transfer learning)
- **Dataset**: PlantDoc — 27 classes of healthy and diseased leaves
- **Input**: Leaf image (224×224 RGB)
- **Output**: Disease class + confidence score

### Crop Price Prediction
- **Algorithms**: XGBoost, Random Forest
- **Crops Supported**: Tomato, Onion, Wheat, Banana, Carrot
- **Features**: Historical prices, seasonal patterns, weather correlation
- **Output**: Predicted price + trend graph

### Weather Forecasting
- **Method**: Time-series ML on historical weather data
- **Output**: Temperature, humidity, rainfall predictions + extreme weather alerts

### Soil Type Detection
- **Architecture**: CNN classifier
- **Classes**: Alluvial soil, Black Soil, Clay soil, Red soil
- **Input**: Soil image (180×180 RGB)
- **Output**: Soil type + confidence + crop/care recommendations

---

## 🔍 Explainable AI (XAI)

SmartCropX implements two XAI techniques to make AI predictions transparent:

### Grad-CAM (Gradient-weighted Class Activation Mapping)
- Generates **heatmap overlays** on leaf/soil images highlighting the regions the model focused on
- Helps farmers understand *why* a disease or soil type was detected
- Implemented via `xai_gradcam.py` using tf-keras-vis

### SHAP (SHapley Additive exPlanations)
- Shows **feature importance** for price predictions
- Visualizes which factors (historical price, weather, season) most influenced the prediction
- Implemented via `xai_shap.py`

---

## 👥 Community Forum

A built-in social platform for farmers, buyers, and administrators.

### Roles
| Role | Capabilities |
|------|-------------|
| **FARMER** | Create posts, comment, like, access predictions |
| **BUYER** | Engage with community, ask about crops |
| **ADMIN** | Full access, moderate content, delete any post/comment |

### Features
- Create, edit, delete posts with tags
- Comment on posts (delete by author or admin)
- Like/unlike posts
- Search posts by keyword, filter by tag, sort by latest or top
- Image upload support
- Auth-aware UI with login/logout and role badges

### Seed Users (auto-created on first startup)

| Name | Email | Password | Role |
|------|-------|----------|------|
| Rajesh Kumar | rajesh@smartcropx.demo | password123 | FARMER |
| Priya Sharma | priya@smartcropx.demo | password123 | BUYER |
| Admin | admin@smartcropx.demo | admin123 | ADMIN |

---

## 🧑‍🌾 Why SmartCropX?

- 🌿 **Reduce crop loss** with early AI-powered disease detection
- 📊 **Make informed decisions** with data-backed price predictions
- 🔍 **Understand AI decisions** through Grad-CAM and SHAP explanations
- 👥 **Learn from the community** via the built-in farmer forum
- 🌦️ **Stay prepared** with ML-based weather forecasting and alerts
- 🌱 **Know your soil** with AI-powered soil classification and crop recommendations

---

## 📄 License

This project is for educational and research purposes.

---

> Built with ❤️ by the SmartCropX team
