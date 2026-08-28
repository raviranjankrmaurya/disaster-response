from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from geoalchemy2.shape import from_shape, to_shape
from shapely.geometry import Polygon, Point

from app.core.database import get_db
from app.core.security import require_api_key
from app.models import models, schemas

router = APIRouter(prefix="/api/zones", tags=["Disaster Zones"])


def _zone_to_dict(zone: models.DisasterZone) -> dict:
    shapely_poly = to_shape(zone.geom)
    centroid = shapely_poly.centroid
    return {
        "id": zone.id,
        "name": zone.name,
        "disaster_event": zone.disaster_event,
        "population_estimate": zone.population_estimate,
        "vulnerable_population_pct": zone.vulnerable_population_pct,
        "severity": zone.severity,
        "centroid_lat": centroid.y,
        "centroid_lon": centroid.x,
        "polygon": [[x, y] for x, y in shapely_poly.exterior.coords],
    }


@router.post("/", response_model=schemas.DisasterZoneOut, dependencies=[Depends(require_api_key)])
def create_zone(zone: schemas.DisasterZoneCreate, db: Session = Depends(get_db)):
    polygon = Polygon(zone.coordinates)
    db_zone = models.DisasterZone(
        name=zone.name,
        disaster_event=zone.disaster_event,
        geom=from_shape(polygon, srid=4326),
        population_estimate=zone.population_estimate,
        vulnerable_population_pct=zone.vulnerable_population_pct,
        severity=zone.severity,
    )
    db.add(db_zone)
    db.commit()
    db.refresh(db_zone)
    return _zone_to_dict(db_zone)


@router.get("/", response_model=list[schemas.DisasterZoneOut])
def list_zones(db: Session = Depends(get_db)):
    zones = db.query(models.DisasterZone).all()
    return [_zone_to_dict(z) for z in zones]


@router.get("/{zone_id}", response_model=schemas.DisasterZoneOut)
def get_zone(zone_id: int, db: Session = Depends(get_db)):
    zone = db.query(models.DisasterZone).filter(models.DisasterZone.id == zone_id).first()
    if not zone:
        raise HTTPException(status_code=404, detail="Zone not found")
    return _zone_to_dict(zone)


depot_router = APIRouter(prefix="/api/depots", tags=["Resource Depots"])


def _depot_to_dict(depot: models.ResourceDepot) -> dict:
    point = to_shape(depot.geom)
    return {
        "id": depot.id,
        "name": depot.name,
        "latitude": point.y,
        "longitude": point.x,
        "road_accessible": bool(depot.road_accessible),
    }


@depot_router.post("/", dependencies=[Depends(require_api_key)])
def create_depot(depot: schemas.ResourceDepotCreate, db: Session = Depends(get_db)):
    point = Point(depot.longitude, depot.latitude)
    db_depot = models.ResourceDepot(
        name=depot.name,
        geom=from_shape(point, srid=4326),
        road_accessible=int(depot.road_accessible),
    )
    db.add(db_depot)
    db.commit()
    db.refresh(db_depot)
    return {"id": db_depot.id, "name": db_depot.name}


@depot_router.get("/")
def list_depots(db: Session = Depends(get_db)):
    depots = db.query(models.ResourceDepot).all()
    return [_depot_to_dict(d) for d in depots]


@depot_router.post("/stock", dependencies=[Depends(require_api_key)])
def add_stock(stock: schemas.ResourceStockCreate, db: Session = Depends(get_db)):
    db_stock = models.ResourceStock(**stock.model_dump())
    db.add(db_stock)
    db.commit()
    db.refresh(db_stock)
    return {"id": db_stock.id, "status": "added"}
