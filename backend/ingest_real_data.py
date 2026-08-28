"""
Real disaster data ingestion — USGS earthquakes + GDACS alerts, filtered
to South Asia. Both are public feeds, no API key needed.

Run after the backend is up:
    python ingest_real_data.py
"""

import os
import requests
import xml.etree.ElementTree as ET
from dotenv import load_dotenv

load_dotenv()

API_BASE = os.getenv("API_BASE", "http://localhost:8000")
API = f"{API_BASE}/api/zones/"
API_KEY = os.getenv("API_KEY", "change-me-in-env")
HEADERS = {"X-API-Key": API_KEY}

USGS_FEED = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_month.geojson"
GDACS_FEED = "https://www.gdacs.org/xml/rss.xml"


def square_around(lon, lat, half_deg=0.15):
    return [
        [lon - half_deg, lat - half_deg],
        [lon + half_deg, lat - half_deg],
        [lon + half_deg, lat + half_deg],
        [lon - half_deg, lat + half_deg],
        [lon - half_deg, lat - half_deg],
    ]


def in_south_asia(lat, lon):
    return 6 <= lat <= 37 and 68 <= lon <= 98


def magnitude_to_severity(mag):
    if mag >= 7:
        return "critical"
    if mag >= 6:
        return "high"
    if mag >= 5:
        return "moderate"
    return "low"


def gdacs_level_to_severity(level):
    return {"Red": "critical", "Orange": "high", "Green": "moderate"}.get(level, "moderate")


def ingest_usgs():
    print("Fetching USGS earthquakes (last month, South Asia region)...")
    resp = requests.get(USGS_FEED, timeout=15)
    resp.raise_for_status()
    data = resp.json()

    count = 0
    for feature in data.get("features", []):
        props = feature["properties"]
        lon, lat = feature["geometry"]["coordinates"][:2]
        if not in_south_asia(lat, lon):
            continue
        mag = props.get("mag") or 0
        place = props.get("place", "Unknown location")

        zone = {
            "name": f"EQ: {place}"[:80],
            "disaster_event": f"Earthquake M{mag}",
            "coordinates": square_around(lon, lat),
            "population_estimate": 10000,
            "vulnerable_population_pct": 0.2,
            "severity": magnitude_to_severity(mag),
        }
        r = requests.post(API, json=zone, headers=HEADERS)
        print(f"  {zone['name']} -> {r.status_code}")
        count += 1
    print(f"USGS: {count} zones ingested.\n")


def ingest_gdacs():
    print("Fetching GDACS active alerts (South Asia region)...")
    resp = requests.get(GDACS_FEED, timeout=15)
    resp.raise_for_status()

    ns = {
        "geo": "http://www.w3.org/2003/01/geo/wgs84_pos#",
        "gdacs": "http://www.gdacs.org",
        "georss": "http://www.georss.org/georss",
    }
    root = ET.fromstring(resp.content)

    count = 0
    for item in root.iter("item"):
        title = item.findtext("title", default="Unknown event")
        alert_level = item.findtext("gdacs:alertlevel", namespaces=ns, default="Green")

        # GDACS's real feed uses <georss:point>lat lon</georss:point> —
        # a single combined string, not separate geo:lat/geo:long elements
        # (that's the older/USGS-style format). Support both.
        lat, lon = None, None
        point_text = item.findtext("georss:point", namespaces=ns, default=None)
        if point_text:
            parts = point_text.strip().split()
            if len(parts) == 2:
                lat, lon = float(parts[0]), float(parts[1])
        if lat is None:
            lat_text = item.findtext("geo:lat", namespaces=ns, default=None)
            lon_text = item.findtext("geo:long", namespaces=ns, default=None)
            if lat_text is not None and lon_text is not None:
                lat, lon = float(lat_text), float(lon_text)

        if lat is None or lon is None:
            continue
        if not in_south_asia(lat, lon):
            continue
        zone = {
            "name": title[:80],
            "disaster_event": title[:120],
            "coordinates": square_around(lon, lat),
            "population_estimate": 15000,
            "vulnerable_population_pct": 0.2,
            "severity": gdacs_level_to_severity(alert_level),
        }
        r = requests.post(API, json=zone, headers=HEADERS)
        print(f"  {zone['name']} -> {r.status_code}")
        count += 1
    print(f"GDACS: {count} zones ingested.\n")


if __name__ == "__main__":
    ingest_usgs()
    ingest_gdacs()
