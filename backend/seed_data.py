"""
Seed script — inserts sample disaster zones.
    python seed_data.py                                          # local
    API_BASE=https://your-app.onrender.com python seed_data.py   # deployed
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_BASE = os.getenv("API_BASE", "http://localhost:8000")
API = f"{API_BASE}/api/zones/"
API_KEY = os.getenv("API_KEY", "change-me-in-env")
HEADERS = {"X-API-Key": API_KEY}

sample_zones = [
    {
        "name": "Kochi Riverside Sector",
        "disaster_event": "Kerala Floods 2018",
        "coordinates": [[76.26, 9.93], [76.30, 9.93], [76.30, 9.98], [76.26, 9.98], [76.26, 9.93]],
        "population_estimate": 42000,
        "vulnerable_population_pct": 0.22,
        "severity": "critical",
    },
    {
        "name": "Chennai Adyar Basin",
        "disaster_event": "Chennai Floods 2015",
        "coordinates": [[80.24, 13.00], [80.28, 13.00], [80.28, 13.04], [80.24, 13.04], [80.24, 13.00]],
        "population_estimate": 31000,
        "vulnerable_population_pct": 0.18,
        "severity": "high",
    },
    {
        "name": "Wayanad Hill Cluster",
        "disaster_event": "Kerala Floods 2018",
        "coordinates": [[76.08, 11.60], [76.12, 11.60], [76.12, 11.64], [76.08, 11.64], [76.08, 11.60]],
        "population_estimate": 9500,
        "vulnerable_population_pct": 0.31,
        "severity": "moderate",
    },
]

if __name__ == "__main__":
    print(f"Seeding against: {API_BASE}")
    for zone in sample_zones:
        resp = requests.post(API, json=zone, headers=HEADERS)
        print(zone["name"], "->", resp.status_code)
