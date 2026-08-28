# Cloud Deployment Guide

Stack (all free, no credit card): **Supabase** (DB) + **Render** (backend) + **Vercel** (frontend).

## Step 1 — Database (Supabase)
1. Sign up at supabase.com, create a project.
2. SQL Editor → run: `CREATE EXTENSION IF NOT EXISTS postgis;`
3. Settings → Database → copy the connection string, change `postgresql://` to `postgresql+psycopg://`.

Free tier note: project pauses after 7 days idle — visit the dashboard before a demo.

## Step 2 — Backend (Render)
1. Push `backend/` to GitHub.
2. render.com → New → Web Service → connect repo.
3. Root directory: `backend`. Build: `pip install -r requirements.txt`. Start: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`. Plan: Free.
4. Environment variables: `DATABASE_URL` (from Step 1), `API_KEY` (pick your own), `ALLOWED_ORIGINS` (set after Step 3).
5. Deploy. Test at `https://your-backend.onrender.com/docs`.
6. Seed it: `API_BASE=https://your-backend.onrender.com API_KEY=your-key python seed_data.py`

Free tier note: sleeps after 15 min idle, first request after that takes 30-60s.

## Step 3 — Frontend (Vercel)
1. In `frontend/src/pages/`, point axios calls through the `api.js` wrapper:
   ```bash
   cd frontend/src/pages
   sed -i '' "s/import axios from 'axios'/import api from '..\/api'/" *.jsx
   sed -i '' "s/axios\./api./g" *.jsx
   ```
   (drop `''` after `-i` on Linux)
2. Push `frontend/` to GitHub.
3. vercel.com → Add New → Project → import repo. Root directory: `frontend`.
4. Environment variable: `VITE_API_BASE_URL` = your Render URL from Step 2.
5. Deploy.

## Step 4 — Connect them
Render → backend service → Environment → update `ALLOWED_ORIGINS` to your Vercel URL. Redeploys automatically.

## Limitations of this free setup
- Cold starts (30-60s) after idle — fine for a shared demo link, not instant clicks
- Supabase pauses after 7 days idle
- No custom domain on free tiers
