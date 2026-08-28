from pydantic import BaseModel
from typing import Optional, List
from app.models.models import SeverityLevel, ResourceType, VolunteerStatus


class DisasterZoneCreate(BaseModel):
    name: str
    disaster_event: str
    coordinates: List[List[float]]
    population_estimate: int = 0
    vulnerable_population_pct: float = 0.0
    severity: SeverityLevel = SeverityLevel.moderate


class DisasterZoneOut(BaseModel):
    id: int
    name: str
    disaster_event: str
    population_estimate: int
    vulnerable_population_pct: float
    severity: SeverityLevel
    centroid_lat: Optional[float] = None
    centroid_lon: Optional[float] = None
    polygon: Optional[List[List[float]]] = None

    class Config:
        from_attributes = True


class ResourceStockCreate(BaseModel):
    depot_id: int
    resource_type: ResourceType
    quantity_available: int
    unit: str = "units"


class ResourceDepotCreate(BaseModel):
    name: str
    longitude: float
    latitude: float
    road_accessible: bool = True


class DemandPredictionOut(BaseModel):
    zone_id: int
    zone_name: str
    predicted_food_packets: float
    predicted_water_liters: float
    predicted_medical_kits: float
    predicted_shelter_capacity: float
    confidence_low: float
    confidence_high: float


class VolunteerCreate(BaseModel):
    name: str
    skill: str
    phone: Optional[str] = None
    assigned_zone_id: Optional[int] = None
    status: VolunteerStatus = VolunteerStatus.available


class VolunteerOut(BaseModel):
    id: int
    name: str
    skill: str
    phone: Optional[str]
    assigned_zone_id: Optional[int]
    status: VolunteerStatus

    class Config:
        from_attributes = True


class AllocationRequest(BaseModel):
    resource_type: ResourceType


class AllocationLine(BaseModel):
    depot_id: int
    depot_name: str
    zone_id: int
    zone_name: str
    quantity_allocated: int
    distance_km: Optional[float] = None
    duration_min: Optional[float] = None
    route_source: Optional[str] = None


class AllocationResult(BaseModel):
    resource_type: ResourceType
    total_demand: int
    total_allocated: int
    unmet_demand: int
    allocations: List[AllocationLine]
