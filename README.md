# RakshaGrid — AI Disaster Relief Coordinator

AI-Based Disaster Response Management System for Resource Allocation and Relief Coordination.

## Folder Structure

```
disaster-response/
├── README.md
├── DEPLOYMENT_GUIDE.md
├── docs/
│   └── DOCUMENTATION.md
├── backend/
│   ├── requirements.txt
│   ├── .env.example
│   ├── render.yaml
│   ├── seed_data.py
│   ├── ingest_real_data.py
│   ├── load_test.py
│   ├── data/historical_disasters.csv       (placeholder data — replace with real)
│   ├── tests/
│   └── app/
│       ├── main.py
│       ├── core/          (database.py, security.py)
│       ├── models/        (models.py, schemas.py)
│       ├── routes/        (zones.py, demand.py, volunteers.py, logistics.py)
│       └── services/      (demand_prediction.py, allocation.py, routing.py)
├── frontend/
│   └── src/
│       ├── api.js
│       ├── main.jsx
│       ├── index.css
│       ├── components/Layout.jsx
│       ├── data/india_outline.json
│       └── pages/         (Dashboard, Incidents, Resources, Volunteers, ReliefMap, Logistics, Reports, Settings)
└── mobile_field_app/       (Flutter — untested on device, see its own README)
```

## Setup — Backend

```bash
cd backend
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Edit `.env`:
```
DATABASE_URL=postgresql+psycopg://YOUR_USERNAME@localhost:5432/disaster_db
API_KEY=your-own-secret-key
```

PostgreSQL + PostGIS (matching versions — don't pin an old Postgres version, PostGIS builds against the latest):
```bash
brew install postgresql postgis
brew services start postgresql
createdb disaster_db
psql disaster_db -c "CREATE EXTENSION IF NOT EXISTS postgis;"
```

Run:
```bash
uvicorn app.main:app --reload
python seed_data.py          # sample data
pytest tests/ -v              # should show 12 passed
```

## Setup — Frontend

```bash
cd frontend
npm install
npm run dev
```

## What Works (verified)

- Zone/depot/volunteer CRUD, PostGIS-backed geospatial storage
- Demand prediction (RandomForest) — trained on placeholder CSV, swap for real data
- **AI allocation engine** (OR-Tools) — severity + road-accessibility + real route
  distance (OSRM) aware. Verified: critical zones get priority under shortage,
  road-inaccessible depots deprioritized (see `backend/tests/`)
- Relief map — official India boundary (Survey of India, via DataMeet), zone
  polygons, severity-colored markers
- Dashboard, Incidents, Resources, Volunteers, Logistics pages — all connected
  to live backend data
- Load testing setup (Locust), 12 automated tests (pytest), all passing
- Mobile field app (Flutter) — built, **not yet run on a device**

## Known Gaps (honest list)

- Historical training data is placeholder, not verified real figures — biggest gap
- No grid-cell severity classification (zones are event-based polygons)
- No multi-stop route optimization (single depot→zone legs only)
- No post-event analytics/situation reports (placeholder page)
- No cloud deployment yet — see `DEPLOYMENT_GUIDE.md` to do it yourself
- No automated cross-browser/mobile responsiveness testing
- No user authentication (API-key scheme only)

See `docs/DOCUMENTATION.md` for full architecture, API reference, and model evaluation.
