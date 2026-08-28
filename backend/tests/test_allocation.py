import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.services.allocation import allocate_resources


def test_no_depots_returns_empty():
    result = allocate_resources([], [{"zone_id": 1, "zone_name": "A", "demand": 100, "severity": "critical"}])
    assert result == []


def test_no_zones_returns_empty():
    result = allocate_resources([{"depot_id": 1, "depot_name": "D1", "quantity_available": 100}], [])
    assert result == []


def test_sufficient_stock_covers_all_demand():
    depots = [{"depot_id": 1, "depot_name": "D1", "quantity_available": 1000}]
    zones = [
        {"zone_id": 1, "zone_name": "Z1", "demand": 300, "severity": "critical"},
        {"zone_id": 2, "zone_name": "Z2", "demand": 200, "severity": "high"},
    ]
    result = allocate_resources(depots, zones)
    total_allocated = sum(a["quantity_allocated"] for a in result)
    assert total_allocated == 500


def test_insufficient_stock_prioritizes_critical_zone():
    depots = [{"depot_id": 1, "depot_name": "D1", "quantity_available": 100}]
    zones = [
        {"zone_id": 1, "zone_name": "Critical Zone", "demand": 100, "severity": "critical"},
        {"zone_id": 2, "zone_name": "Moderate Zone", "demand": 100, "severity": "moderate"},
    ]
    result = allocate_resources(depots, zones)
    critical_allocation = next((a["quantity_allocated"] for a in result if a["zone_id"] == 1), 0)
    moderate_allocation = next((a["quantity_allocated"] for a in result if a["zone_id"] == 2), 0)
    assert critical_allocation == 100
    assert moderate_allocation == 0


def test_never_allocates_more_than_depot_stock():
    depots = [{"depot_id": 1, "depot_name": "D1", "quantity_available": 50}]
    zones = [{"zone_id": 1, "zone_name": "Z1", "demand": 500, "severity": "critical"}]
    result = allocate_resources(depots, zones)
    total_allocated = sum(a["quantity_allocated"] for a in result)
    assert total_allocated <= 50


def test_never_allocates_more_than_zone_demand():
    depots = [{"depot_id": 1, "depot_name": "D1", "quantity_available": 500}]
    zones = [{"zone_id": 1, "zone_name": "Z1", "demand": 50, "severity": "critical"}]
    result = allocate_resources(depots, zones)
    total_allocated = sum(a["quantity_allocated"] for a in result)
    assert total_allocated <= 50


def test_road_inaccessible_depot_deprioritized():
    depots = [
        {"depot_id": 1, "depot_name": "Far", "quantity_available": 50, "road_accessible": False},
        {"depot_id": 2, "depot_name": "Near", "quantity_available": 50, "road_accessible": True},
    ]
    zones = [{"zone_id": 1, "zone_name": "Z1", "demand": 50, "severity": "critical"}]
    routes = {
        (1, 1): {"distance_km": 10, "duration_min": 20, "source": "osrm"},
        (2, 1): {"distance_km": 10, "duration_min": 20, "source": "osrm"},
    }
    result = allocate_resources(depots, zones, routes)
    accessible_alloc = next((a["quantity_allocated"] for a in result if a["depot_id"] == 2), 0)
    assert accessible_alloc == 50
