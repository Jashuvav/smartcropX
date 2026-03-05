# SmartCropX — Developer Documentation

## Architecture

```
Frontend (React 19 / CRA / Tailwind CSS 3)  ⟶  Backend (FastAPI / Python 3.13)
                                                       │
                                                  SQLite (SQLAlchemy 2.0)
                                                       │
                                            ML Models (TensorFlow / XGBoost)
```

| Layer        | Tech                           | Port  |
|-------------|--------------------------------|-------|
| Frontend    | React 19, react-router-dom 6, framer-motion, Tailwind 3 | 3000 |
| Backend     | FastAPI, Uvicorn               | 8001  |
| Database    | SQLite via SQLAlchemy 2.0      | file  |
| ML          | TensorFlow 2 (Soil CNN, PlantDoc CNN) | —     |

---

## Database (SQLite)

The app uses a single **SQLite** database file located at:

```
backend/data/smartcropx.db
```

### Tables

| Table            | Purpose                                 |
|------------------|-----------------------------------------|
| `users`          | Registered users (id, full_name, email, hashed_password, role) |
| `posts`          | Community forum posts (id, title, body, tags, image_url, author_id, created_at) |
| `comments`       | Post comments (id, body, post_id, author_id, created_at) |
| `likes`          | Post likes (id, post_id, user_id)       |
| `bookmarks`      | User bookmarks (id, post_id, user_id)   |
| `crop_recommendation_history` | Stored crop recommendation results |

Tables are auto-created on startup via `Base.metadata.create_all()`.  
Seed data (`seed_if_empty()`) inserts 3 demo users + 5 posts on first run.

### Seed Accounts

| Role        | Email                      | Password    |
|-------------|----------------------------|-------------|
| ADMIN       | admin@smartcropx.com       | Admin@123   |
| FARMER      | farmer@smartcropx.com      | Farmer@123  |
| AGRONOMIST  | agronomist@smartcropx.com  | Agro@123    |

---

## Roles & RBAC

Three roles: **FARMER**, **AGRONOMIST**, **ADMIN**.

| Feature                | FARMER | AGRONOMIST | ADMIN |
|------------------------|--------|------------|-------|
| Disease Detection      | ✅     | ✅         | ✅    |
| Crop Recommendation    | ✅     | ✅         | ✅    |
| Weather Forecast       | ✅     | ✅         | ✅    |
| Community              | ✅     | ✅         | ✅    |
| Soil Detection         | ✅     | ❌         | ✅    |
| Pesticide Recommend.   | ✅     | ❌         | ✅    |

Frontend enforces via `<ProtectedRoute roles={[…]}>` and dashboard card filtering.  
Backend enforces via `require_role()` dependency.

---

## Health Endpoints

| Endpoint           | Method | Auth | Description                              |
|--------------------|--------|------|------------------------------------------|
| `/health`          | GET    | No   | Simple status check                      |
| `/api/health`      | GET    | No   | Same as above                            |
| `/healthz`         | GET    | No   | Detailed health with model load status   |
| `/api/db/health`   | GET    | No   | Database connectivity + table row counts |

---

## API Endpoints (Summary)

### Auth
- `POST /api/auth/register` — Create account
- `POST /api/auth/login` — Login, get JWT
- `GET  /api/auth/me` — Current user profile

### ML Predictions
- `POST /predict` — Plant disease detection (image upload)
- `POST /predict-soil` — Soil type classification (image upload)
- `GET  /weather-forecast` — 7-day ML weather forecast
- `GET  /weather-current?city=` — Live weather from OpenWeatherMap
- `GET  /weather-alerts` — Weather alert generation

### Explainable AI (XAI)
- `POST /api/disease/explain` — Grad-CAM heatmap for plant image
- `POST /api/soil/explain` — Grad-CAM + feature explanation for soil

### Recommendations
- `POST /api/recommend/crop` — AI crop recommendation
- `POST /api/recommend/soil` — Soil-based recommendation
- `GET  /api/recommend/health` — Recommendation service health

### Pesticide
- `POST /api/pesticide/recommend` — Pesticide recommendation
- `GET  /api/pesticide/diseases` — List of diseases
- `GET  /api/pesticide/crops` — List of crops
- `GET  /api/pesticide/health` — Pesticide service health

### Community
- `GET  /api/community/posts` — List posts (search, tag, sort)
- `POST /api/community/posts` — Create post
- `GET  /api/community/posts/:id` — Get single post
- `PATCH /api/community/posts/:id` — Update post
- `DELETE /api/community/posts/:id` — Delete post
- `POST /api/community/posts/:id/comments` — Add comment
- `POST /api/community/posts/:id/like` — Toggle like
- `POST /api/community/upload-image` — Upload community image

---

## Running Locally

### Prerequisites
- Python 3.13+ with venv at `.venv`
- Node.js 18+

### Backend
```powershell
$env:TF_ENABLE_ONEDNN_OPTS=0
.\.venv\Scripts\python.exe -m uvicorn backend.main:app --host 0.0.0.0 --port 8001
```

### Frontend
```powershell
cd frontend
npm install
npm start   # runs on port 3000
```

### Reset Database
Delete `backend/data/smartcropx.db` and restart backend — seed data will be recreated.

---

## Project Structure (Key Files)

```
backend/
  main.py                  # FastAPI app, ML endpoints
  community/
    routes.py              # Auth + community CRUD + seed data
    models.py              # SQLAlchemy ORM models (User, Post, Comment, Like)
    auth.py                # JWT creation, password hashing, require_role()
    database.py            # SQLAlchemy engine + SessionLocal
    schemas.py             # Pydantic request/response schemas
  recommendation/          # Crop recommendation module
  pesticide/               # Pesticide recommendation module
  models/                  # Trained ML model files (.keras)
  scripts/                 # Training scripts, data preprocessing
  data/                    # CSV datasets, SQLite DB file

frontend/
  tsconfig.json            # TypeScript config (baseUrl: "src")
  src/
    App.js                 # Router + home page layout
    lib/utils.ts           # shadcn cn() utility (clsx + tailwind-merge)
    components/
      ui/                  # shadcn-style reusable UI components
        glare-card.tsx     # GlareCard – 3D holographic hover effect
      ProtectedRoute.jsx   # Role-gated route wrapper
    context/AuthContext.js  # JWT auth provider, authAxios
    config/api.js           # API URL + endpoint constants
    pages/                 # All page components
    data/newsData.json     # Static news articles
```

### Why `/components/ui`?

We follow the **shadcn/ui** convention of placing reusable primitives under
`src/components/ui/`. This matters because:

- **shadcn CLI** (`npx shadcn@latest add <component>`) writes files there by
  default, so adding Button, Card, Dialog etc. later "just works".
- Keeps a clear separation between *project pages* (`pages/`) and *generic
  UI primitives* (`components/ui/`).
- Any developer familiar with shadcn conventions knows exactly where to look.
