# 🌿 SmartCropX — AI-Powered Smart Agriculture Platform

**SmartCropX** is a full-stack smart agriculture platform combining **AI/ML**, **Deep Learning**, **Explainable AI (XAI)**, and **Blockchain** technology to help farmers make data-driven decisions — from detecting plant diseases to predicting market prices, monitoring weather, analyzing soil, and trading crops transparently.

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
- [Blockchain Marketplace](#-blockchain-marketplace)
- [Community Forum](#-community-forum)
- [Screenshots](#-screenshots)

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🌿 **Plant Disease Detection** | Upload a leaf image → AI identifies the disease using EfficientNetB4 deep learning model |
| 📈 **Crop Price Prediction** | Predict future market prices for crops (Tomato, Onion, Wheat, Banana, Carrot) using XGBoost & Random Forest |
| 🌦️ **Weather Forecasting & Alerts** | ML-based weather prediction with real-time alerts for extreme conditions |
| 🌱 **Soil Quality Detection** | Classify soil type from images using a trained CNN model |
| 🔗 **Blockchain Marketplace** | Buy/sell crops securely via Ethereum smart contracts with full transaction traceability |
| 👥 **Community Forum** | Post, comment, like, and share knowledge — with JWT auth and role-based access (Farmer/Buyer/Admin) |
| 🔍 **Explainable AI (XAI)** | Grad-CAM heatmaps and SHAP feature explanations for model transparency |
| 🤖 **AI Chatbot** | Rule-based XAI assistant — ask about crops, diseases, soil, prices, and how SmartCropX AI works (no API key needed) |
| 📱 **Modern Responsive UI** | React + Tailwind CSS with smooth navigation, animated dashboard, and mobile-friendly design |

---

## 🧰 Tech Stack

| Layer | Technologies |
|-------|-------------|
| **Frontend** | React 19, Tailwind CSS 3, React Router 6, Axios, Framer Motion, Lucide Icons, Web3.js |
| **Backend** | FastAPI, Python 3.13, Uvicorn, Pydantic |
| **AI / ML** | TensorFlow, Keras (EfficientNetB4), Scikit-learn, XGBoost, OpenCV |
| **XAI** | Grad-CAM (tf-keras-vis), SHAP |
| **Auth** | JWT (HS256) via python-jose, passlib + bcrypt |
| **Database** | SQLite + SQLAlchemy 2.0 ORM |
| **Blockchain** | Solidity, Truffle, Ganache, Ethereum Testnet |
| **Data Tools** | Pandas, NumPy, Matplotlib |

---

## 📁 Project Structure

```
SmartCropX/
├── backend/
│   ├── main.py                  # FastAPI app with all routers
│   ├── chatbot.py               # Rule-based XAI chatbot engine
│   ├── start.py                 # Server entry point (port 8001)
│   ├── .env.example             # Environment variable template
│   ├── community/               # Community forum module
│   │   ├── models.py            # SQLAlchemy models (User, Post, Comment, Like)
│   │   ├── schemas.py           # Pydantic request/response schemas
│   │   ├── auth.py              # JWT authentication & password hashing
│   │   ├── routes.py            # Community & auth API routes
│   │   └── database.py          # SQLite database setup
│   ├── scripts/
│   │   ├── predict_plantdoc.py  # Plant disease prediction
│   │   ├── predict_soil.py      # Soil type classification
│   │   ├── predict_weather.py   # Weather forecasting
│   │   ├── predict_with_graph.py # Crop price prediction + graph
│   │   ├── xai_gradcam.py       # Grad-CAM explainability
│   │   ├── xai_shap.py          # SHAP explainability
│   │   └── ...training scripts
│   ├── models/                  # Trained .keras model files
│   ├── data/                    # CSV datasets + SQLite DB
│   └── blockchain/              # Solidity smart contracts
├── frontend/
│   ├── src/
│   │   ├── App.js               # Routes & AuthProvider
│   │   ├── context/AuthContext.js
│   │   └── pages/
│   │       ├── Header.jsx       # Navigation bar
│   │       ├── AgriDashboard.jsx # Main dashboard (7 feature cards)
│   │       ├── OrganicFarmUI.jsx # Landing / About section
│   │       ├── AgriNewsSection.jsx
│   │       ├── ContactUs.jsx    # Contact form + footer
│   │       ├── CommunityFeed.jsx
│   │       ├── CreatePost.jsx
│   │       ├── PostDetail.jsx
│   │       ├── Login.jsx / Register.jsx
│   │       └── ...feature pages
│   ├── contracts/               # Solidity contracts (frontend copy)
│   └── public/
├── README.md
├── .gitignore
└── build.sh / render.yaml       # Deployment config
```

---

## 🚀 Getting Started

### Prerequisites
- **Python 3.10+**
- **Node.js 18+** and npm
- **Git** (with Git LFS for model files)

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

# (Optional) Create a .env file from the template
cp .env.example .env   # edit if needed; chatbot works without any API keys
```

### 3. Start the Backend Server

```bash
python start.py
# Server runs at http://localhost:8001
# API docs at http://localhost:8001/docs
```

### Quick Verification (curl)

```bash
# Health check
curl http://localhost:8001/api/health

# Chat with the AI assistant
curl -X POST http://localhost:8001/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "hello", "sessionId": "test-1"}'

# Chatbot health
curl http://localhost:8001/api/chat/health
```

### 4. Frontend Setup

```bash
cd frontend
npm install
npm start
# App runs at http://localhost:3000
```

### 5. Blockchain (Optional)

```bash
# Install Truffle & Ganache globally
npm install -g truffle ganache-cli

# Start Ganache
ganache-cli

# Deploy contracts
cd frontend
truffle migrate --reset
```

---

## 📡 API Reference

Base URL: `http://localhost:8001`

### Core Prediction Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/predict` | Plant disease detection (upload image) |
| POST | `/predict-soil` | Soil type classification (upload image) |
| POST | `/predict-price` | Crop price prediction |
| GET | `/weather` | Weather forecast & alerts |
| POST | `/xai/gradcam` | Grad-CAM heatmap for disease prediction |
| POST | `/xai/shap` | SHAP explanation for price prediction |

### Chatbot Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/chat` | Send a message to the XAI chatbot (`{ "message": "...", "sessionId": "..." }`) |
| GET | `/api/chat/health` | Chatbot sub-system health check |

### Health Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` or `/api/health` | Basic health check |
| GET | `/healthz` | Detailed health check (model status + chatbot) |

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
| GET | `/api/community/posts/{id}/comments` | — | List comments on a post |
| POST | `/api/community/posts/{id}/comments` | ✅ | Add a comment |
| DELETE | `/api/community/comments/{id}` | ✅ | Delete a comment |
| POST | `/api/community/posts/{id}/like` | ✅ | Toggle like on a post |
| POST | `/api/community/upload` | ✅ | Upload an image |

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

### Soil Quality Detection
- **Architecture**: CNN classifier
- **Input**: Soil image
- **Output**: Soil type classification

---

## 🔍 Explainable AI (XAI)

SmartCropX implements two XAI techniques to make AI predictions transparent:

### Grad-CAM (Gradient-weighted Class Activation Mapping)
- Generates **heatmap overlays** on leaf images highlighting the regions the model focused on
- Helps farmers understand *why* a disease was detected
- Implemented via `xai_gradcam.py` using tf-keras-vis

### SHAP (SHapley Additive exPlanations)
- Shows **feature importance** for price predictions
- Visualizes which factors (historical price, weather, season) most influenced the prediction
- Implemented via `xai_shap.py`

---

## 🔗 Blockchain Marketplace

- **Smart Contracts**: Written in Solidity (`Marketplace.sol`, `StorageManagement.sol`)
- **Framework**: Truffle for compilation and deployment
- **Local Blockchain**: Ganache for testing
- **Frontend Integration**: Web3.js connects React UI to Ethereum contracts
- **Features**:
  - List crops for sale with price and quantity
  - Buyers can purchase crops with full transaction history
  - All transactions recorded on-chain for transparency and trust

---

## 👥 Community Forum

A built-in social platform for farmers, buyers, and administrators.

### Roles
| Role | Capabilities |
|------|-------------|
| **FARMER** | Create posts, comment, like, share farming tips |
| **BUYER** | Engage with community, ask about crops |
| **ADMIN** | Moderate content, delete any post/comment |

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

### Quick Test

```bash
# Login
curl -X POST http://localhost:8001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"rajesh@smartcropx.demo","password":"password123"}'

# List posts
curl http://localhost:8001/api/community/posts

# Create post (use token from login response)
curl -X POST http://localhost:8001/api/community/posts \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"title":"My first post","body":"Hello community!"}'
```

---

## 🧑‍🌾 Why SmartCropX?

- 🌿 **Reduce crop loss** with early AI-powered disease detection
- 📊 **Make informed decisions** with data-backed price predictions
- 🔗 **Trade with confidence** using blockchain-verified transactions
- 🔍 **Understand AI decisions** through Grad-CAM and SHAP explanations
- 👥 **Learn from the community** via the built-in farmer forum
- 🌦️ **Stay prepared** with ML-based weather forecasting and alerts

---

## 📸 Screenshots

![Screenshot 2025-03-14 173845](https://github.com/user-attachments/assets/8ceb7a78-cc62-46e4-af5a-37f3de5fec85)

![Screenshot 2025-03-14 173013](https://github.com/user-attachments/assets/829c1008-fc51-471f-8f3a-30bf3865ecff)

![Screenshot 2025-03-14 173025](https://github.com/user-attachments/assets/8eeff232-9309-4bc3-8979-37ddc985283d)

![Screenshot 2025-03-14 173037](https://github.com/user-attachments/assets/64f112cc-7b09-455c-a496-5ae90efa9690)

![Screenshot 2025-03-14 173054](https://github.com/user-attachments/assets/316b6e62-7cc5-4424-9001-08a68494a020)

![Screenshot 2025-03-14 173118](https://github.com/user-attachments/assets/6bf31ecc-fb62-4256-b808-529e372c16ce)

![Screenshot 2025-03-14 173125](https://github.com/user-attachments/assets/49ca73e1-9577-4725-bd09-d060ba890043)

![Screenshot 2025-03-14 173143](https://github.com/user-attachments/assets/8893d77f-2190-4a4d-b73a-08ee33aeeb5c)

![Screenshot 2025-03-14 173153](https://github.com/user-attachments/assets/91d9e080-a772-448b-9806-42a4f4b98656)

![Screenshot 2025-03-14 173200](https://github.com/user-attachments/assets/f5a863c2-eb7a-4633-8f39-b3eba45020d6)

![Screenshot 2025-03-14 173215](https://github.com/user-attachments/assets/e7e35d14-70bb-4be8-b986-8f764f172ebe)

![Screenshot 2025-03-14 173227](https://github.com/user-attachments/assets/c96f35c6-2f28-412a-80c8-a6875bcf9cac)

![Screenshot 2025-03-14 173247](https://github.com/user-attachments/assets/01869df7-0e05-4c1d-9ebf-121355e4cae1)

![Screenshot 2025-03-14 173258](https://github.com/user-attachments/assets/9d72109a-df79-4aa6-b084-28a5a6b17483)

![Screenshot 2025-03-14 173317](https://github.com/user-attachments/assets/92deda2b-6853-4c3a-b72b-31b990658ec4)

![Screenshot 2025-03-14 173331](https://github.com/user-attachments/assets/263c0353-8a53-4dd1-972a-440625aa44d6)

![Screenshot 2025-03-14 173341](https://github.com/user-attachments/assets/ad9c7738-db4e-43f6-a9f3-a087b7ab9c9c)

![Screenshot 2025-03-14 173358](https://github.com/user-attachments/assets/0126eb0a-0db6-47f9-b585-8b7adf84d49e)

![Screenshot 2025-03-14 173405](https://github.com/user-attachments/assets/4d3be53c-6903-4f8b-8777-3c6decfff14b)

![Screenshot 2025-03-14 173413](https://github.com/user-attachments/assets/0bf06921-6b60-4d04-9443-f52cfdb62b21)

![Screenshot 2025-03-14 173419](https://github.com/user-attachments/assets/86aa8308-0525-448b-9aff-5b1f57c8d4f5)

![Screenshot 2025-03-14 173438](https://github.com/user-attachments/assets/204f1bde-82c3-46c1-b5e2-32e1df0702c5)

![Screenshot 2025-03-14 173452](https://github.com/user-attachments/assets/19ccd31c-1b70-4133-8281-18c82639519b)

![Screenshot 2025-03-14 173500](https://github.com/user-attachments/assets/b938ea86-3349-4c71-897a-acb53c0c5a1a)

![Screenshot 2025-03-14 173508](https://github.com/user-attachments/assets/b352905c-4d1e-4afa-a663-7ef1b681460f)

![Screenshot 2025-03-14 173533](https://github.com/user-attachments/assets/7d6892c6-ddfc-4284-a4b4-6fe646003ad8)

![Screenshot 2025-03-14 173547](https://github.com/user-attachments/assets/c26447af-496d-4d0d-8d10-987cf7427d72)

![Screenshot 2025-03-14 173605](https://github.com/user-attachments/assets/113c3b5f-3fdf-4eba-b68f-0a1e430c905a)

![Screenshot 2025-03-14 173711](https://github.com/user-attachments/assets/2da65a81-e711-436e-9e3b-e313fa331162)

![Screenshot 2025-03-14 173735](https://github.com/user-attachments/assets/e1f2db46-fd62-4659-964b-3332d4c80a62)

![Screenshot 2025-03-14 173824](https://github.com/user-attachments/assets/7d189e2e-3ff5-4543-b394-e1eb0ce28dc4)

![Screenshot 2025-03-14 174115](https://github.com/user-attachments/assets/2b692248-8144-4c9a-b04d-366842391ae8)

![Screenshot 2025-03-14 174123](https://github.com/user-attachments/assets/9778c7fa-0df3-4ba0-9e66-c21f37f0a505)

![Screenshot 2025-03-14 173143](https://github.com/user-attachments/assets/bf224190-39f5-4e77-8b89-06147ab5320e)

![Screenshot 2025-03-14 174044](https://github.com/user-attachments/assets/254c2953-9804-4d8c-ae3d-e4a21d7128f9)

![Screenshot 2025-03-14 174051](https://github.com/user-attachments/assets/81c04ce2-1aa8-4da0-a65d-0fa6514adca3)

![Screenshot 2025-03-14 174059](https://github.com/user-attachments/assets/215e09b2-d517-4caa-9e84-2f13320d88a8)

![Screenshot 2025-03-14 174106](https://github.com/user-attachments/assets/6ffbf2b1-69e6-4202-b88d-7b0e2282ba39)

---

## 📄 License

This project is for educational and research purposes.

---

> Built with ❤️ by the SmartCropX team
