"""
Delivery route generation (depot -> zone) using the free public OSRM
demo server. No API key needed.

Caveats (real, not hidden):
  - OSRM's public demo server has no uptime guarantee, ~1 req/sec limit,
    non-commercial reasonable use only. Self-host OSRM for production.
  - Doesn't know about post-disaster road damage — only `road_accessible`
    on a depot signals that, OSRM's routing itself has no disaster-awareness.
  - Falls back to straight-line (haversine) distance if unreachable, so
    the allocation engine keeps working; flags the result as an estimate.
"""

import math
import requests

OSRM_BASE_URL = "https://router.project-osrm.org/route/v1/driving"
OSRM_TIMEOUT_SECONDS = 5


def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371.0
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return 2 * R * math.asin(math.sqrt(a))


def get_route(depot_lat, depot_lon, zone_lat, zone_lon):
    try:
        url = f"{OSRM_BASE_URL}/{depot_lon},{depot_lat};{zone_lon},{zone_lat}"
        resp = requests.get(
            url,
            params={"overview": "full", "geometries": "geojson"},
            timeout=OSRM_TIMEOUT_SECONDS,
        )
        resp.raise_for_status()
        data = resp.json()
        if data.get("code") != "Ok" or not data.get("routes"):
            raise ValueError("OSRM returned no route")

        route = data["routes"][0]
        coords = route["geometry"]["coordinates"]
        return {
            "distance_km": round(route["distance"] / 1000, 2),
            "duration_min": round(route["duration"] / 60, 1),
            "geometry": [[lat, lon] for lon, lat in coords],
            "source": "osrm",
        }
    except Exception:
        dist = haversine_km(depot_lat, depot_lon, zone_lat, zone_lon)
        assumed_speed_kmh = 35
        return {
            "distance_km": round(dist, 2),
            "duration_min": round((dist / assumed_speed_kmh) * 60, 1),
            "geometry": None,
            "source": "straight_line_fallback",
        }
