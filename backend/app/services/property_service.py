from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.property import Property
from app.schemas.property import PropertyCreate


def create_property(db: Session, payload: PropertyCreate) -> Property:
    property_obj = Property(**payload.model_dump())
    db.add(property_obj)
    db.commit()
    db.refresh(property_obj)
    return property_obj


def list_properties(db: Session) -> list[Property]:
    return list(db.scalars(select(Property).order_by(Property.property_id)).all())
