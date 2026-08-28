# RakshaGrid — Project Documentation

**AI-Based Disaster Response Management System for Resource Allocation and Relief Coordination**

## 1. System Architecture

```
Frontend (React + Vite + React Router)
        |  REST (JSON over HTTP)
Backend (FastAPI, Python 3.12)
        |  SQLAlchemy ORM
PostgreSQL + PostGIS
```

Backend module layout:
```
backend/app/
├── core/       — database connection, API-key auth
├── models/     — SQLAlchemy tables + Pydantic schemas
├── routes/     — zones, depots, demand, volunteers, logistics
└── services/   — demand_prediction (ML), allocation (OR-Tools), routing (OSRM)
```

## 2. API Reference

Base URL (dev): `http://localhost:8000`. Write endpoints (POST/PATCH/DELETE)
require an `X-API-Key` header. Full interactive reference at `/docs`.

| Method | Path | Description |
|---|---|---|
| POST | /api/zones/ | Create a zone |
| GET | /api/zones/ | List zones (includes centroid + polygon) |
| GET | /api/zones/{id} | Get one zone |
| POST | /api/depots/ | Create a depot |
| GET | /api/depots/ | List depots |
| POST | /api/depots/stock | Add stock to a depot |
| GET | /api/demand/{zone_id} | Predicted resource demand |
| POST | /api/volunteers/ | Register a volunteer |
| GET | /api/volunteers/ | List volunteers |
| PATCH | /api/volunteers/{id}/assign/{zone_id} | Assign volunteer to zone |
| DELETE | /api/volunteers/{id} | Remove volunteer |
| POST | /api/logistics/allocate | Run the route-aware allocation engine |

## 3. Model / Algorithm Evaluation

**Demand prediction:** RandomForestRegressor, trained on
`backend/data/historical_disasters.csv` — **placeholder/illustrative
numbers, not verified real data.** Replace before trusting predictions.

**Allocation engine:** OR-Tools CP-SAT, maximizes severity-weighted +
route-practicality-weighted coverage. Verified: critical zones get
priority when supply is short; road-inaccessible depots are
deprioritized (tested in `tests/test_allocation.py`, all passing).

**Route generation:** OSRM public demo server (real road-network
distance/duration), falls back to straight-line distance if unreachable.

## 4. Deployment

See `DEPLOYMENT_GUIDE.md` at the project root for the full walkthrough
(Supabase + Render + Vercel, free tier, no credit card).

## 5. Known Limitations

- Historical training data is placeholder-quality, not verified
- No route optimization for multi-stop deliveries (single depot→zone legs only)
- No grid-cell severity classification — zones are event-based polygons, not a grid
- No automated integration tests (only unit tests for allocation + prediction)
- Mobile app not tested on a device/emulator
- No user authentication — API-key scheme only
- `Base.metadata.create_all()` used instead of proper migrations (Alembic)
