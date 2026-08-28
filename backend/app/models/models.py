from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry
from datetime import datetime
import enum

from app.core.database import Base


class SeverityLevel(str, enum.Enum):
    low = "low"
    moderate = "moderate"
    high = "high"
    critical = "critical"


class ResourceType(str, enum.Enum):
    food = "food"
    water = "water"
    medical_kit = "medical_kit"
    shelter_kit = "shelter_kit"
    rescue_vehicle = "rescue_vehicle"
    personnel = "personnel"


class DisasterZone(Base):
    __tablename__ = "disaster_zones"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    disaster_event = Column(String, nullable=False)
    geom = Column(Geometry(geometry_type="POLYGON", srid=4326), nullable=False)
    population_estimate = Column(Integer, default=0)
    vulnerable_population_pct = Column(Float, default=0.0)
    severity = Column(Enum(SeverityLevel), default=SeverityLevel.moderate)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ResourceDepot(Base):
    __tablename__ = "resource_depots"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    geom = Column(Geometry(geometry_type="POINT", srid=4326), nullable=False)
    road_accessible = Column(Integer, default=1)

    stocks = relationship("ResourceStock", back_populates="depot")


class ResourceStock(Base):
    __tablename__ = "resource_stocks"

    id = Column(Integer, primary_key=True, index=True)
    depot_id = Column(Integer, ForeignKey("resource_depots.id"))
    resource_type = Column(Enum(ResourceType), nullable=False)
    quantity_available = Column(Integer, default=0)
    unit = Column(String, default="units")

    depot = relationship("ResourceDepot", back_populates="stocks")


class VolunteerStatus(str, enum.Enum):
    available = "available"
    deployed = "deployed"
    off_duty = "off_duty"


class Volunteer(Base):
    __tablename__ = "volunteers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    skill = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    assigned_zone_id = Column(Integer, ForeignKey("disaster_zones.id"), nullable=True)
    status = Column(Enum(VolunteerStatus), default=VolunteerStatus.available)
    created_at = Column(DateTime, default=datetime.utcnow)

    assigned_zone = relationship("DisasterZone")
