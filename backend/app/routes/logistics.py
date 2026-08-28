from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from geoalchemy2.shape import to_shape

from app.core.database import get_db
from app.models import models, schemas
from app.services.allocation import allocate_resources
from app.services.demand_prediction import predictor
from app.services.routing import get_route

router = APIRouter(prefix="/api/logistics", tags=["Logistics"])


@router.post("/allocate", response_model=schemas.AllocationResult)
def allocate(request: schemas.AllocationRequest, db: Session = Depends(get_db)):
    stocks = (
        db.query(models.ResourceStock)
        .filter(models.ResourceStock.resource_type == request.resource_type)
        .all()
    )
    depots_stock = []
    depot_locations = {}
    for s in stocks:
        depot_point = to_shape(s.depot.geom)
        depot_locations[s.depot_id] = (depot_point.y, depot_point.x)
        depots_stock.append({
            "depot_id": s.depot_id,
            "depot_name": s.depot.name,
            "quantity_available": s.quantity_available,
            "road_accessible": bool(s.depot.road_accessible),
        })

    zones = db.query(models.DisasterZone).all()
    field_map = {
        "food": "predicted_food_packets",
        "water": "predicted_water_liters",
        "medical_kit": "predicted_medical_kits",
        "shelter_kit": "predicted_shelter_capacity",
    }
    demand_field = field_map.get(request.resource_type.value)

    zones_demand = []
    zone_locations = {}
    for z in zones:
        prediction = predictor.predict(
            population=z.population_estimate,
            vulnerable_pct=z.vulnerable_population_pct,
            severity=z.severity.value,
        )
        demand_qty = int(prediction.get(demand_field, 0)) if demand_field else 0
        if demand_qty > 0:
            zone_point = to_shape(z.geom)
            zone_centroid = zone_point.centroid
            zone_locations[z.id] = (zone_centroid.y, zone_centroid.x)
            zones_demand.append({
                "zone_id": z.id,
                "zone_name": z.name,
                "demand": demand_qty,
                "severity": z.severity.value,
            })

    routes = {}
    for d in depots_stock:
        depot_lat, depot_lon = depot_locations[d["depot_id"]]
        for z in zones_demand:
            zone_lat, zone_lon = zone_locations[z["zone_id"]]
            routes[(d["depot_id"], z["zone_id"])] = get_route(depot_lat, depot_lon, zone_lat, zone_lon)

    allocations = allocate_resources(depots_stock, zones_demand, routes)

    total_demand = sum(z["demand"] for z in zones_demand)
    total_allocated = sum(a["quantity_allocated"] for a in allocations)

    return {
        "resource_type": request.resource_type,
        "total_demand": total_demand,
        "total_allocated": total_allocated,
        "unmet_demand": max(total_demand - total_allocated, 0),
        "allocations": allocations,
    }
