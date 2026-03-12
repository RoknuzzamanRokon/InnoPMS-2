from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from api.deps import get_db
from schemas.property import PropertyCreate, PropertyRead
from services.property_service import create_property, list_properties

router = APIRouter()


@router.post("", response_model=PropertyRead, status_code=status.HTTP_201_CREATED)
def create_property_endpoint(payload: PropertyCreate, db: Session = Depends(get_db)) -> PropertyRead:
    return create_property(db, payload)


@router.get("", response_model=list[PropertyRead])
def list_properties_endpoint(db: Session = Depends(get_db)) -> list[PropertyRead]:
    return list_properties(db)
