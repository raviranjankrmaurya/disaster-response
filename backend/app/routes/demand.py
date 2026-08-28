from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models import models, schemas
from app.services.demand_prediction import predictor

router = APIRouter(prefix="/api/demand", tags=["Demand Prediction"])


@router.get("/{zone_id}", response_model=schemas.DemandPredictionOut)
def predict_demand(zone_id: int, db: Session = Depends(get_db)):
    zone = db.query(models.DisasterZone).filter(models.DisasterZone.id == zone_id).first()
    if not zone:
        raise HTTPException(status_code=404, detail="Zone not found")

    result = predictor.predict(
        population=zone.population_estimate,
        vulnerable_pct=zone.vulnerable_population_pct,
        severity=zone.severity.value,
    )

    return {
        "zone_id": zone.id,
        "zone_name": zone.name,
        **result,
    }
