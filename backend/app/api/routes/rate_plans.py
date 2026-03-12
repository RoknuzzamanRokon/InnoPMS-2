from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.rate_plan import RatePlanCreate, RatePlanRead
from app.services.rate_plan_service import create_rate_plan

router = APIRouter()


@router.post("", response_model=RatePlanRead, status_code=status.HTTP_201_CREATED)
def create_rate_plan_endpoint(payload: RatePlanCreate, db: Session = Depends(get_db)) -> RatePlanRead:
    return create_rate_plan(db, payload)
