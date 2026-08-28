from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from app.core.database import engine, Base
from app.routes import zones, demand, volunteers, logistics

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Disaster Response Management API",
    description="AI-based disaster resource allocation and relief coordination backend",
    version="0.4.0",
)

_default_dev_origins = "http://localhost:5173,http://localhost:5174,http://127.0.0.1:5173,http://127.0.0.1:5174"
origins = os.getenv("ALLOWED_ORIGINS", _default_dev_origins).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(zones.router)
app.include_router(zones.depot_router)
app.include_router(demand.router)
app.include_router(volunteers.router)
app.include_router(logistics.router)


@app.get("/")
def root():
    return {"status": "ok", "service": "disaster-response-api"}
