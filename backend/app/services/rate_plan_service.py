from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models.property import Property
from models.rate_plan import RatePlan
from schemas.rate_plan import RatePlanCreate


def create_rate_plan(db: Session, payload: RatePlanCreate) -> RatePlan:
    property_obj = db.get(Property, payload.property_id)
    if property_obj is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Property not found")

    rate_plan = RatePlan(**payload.model_dump())
    db.add(rate_plan)
    db.commit()
    db.refresh(rate_plan)
    return rate_plan
