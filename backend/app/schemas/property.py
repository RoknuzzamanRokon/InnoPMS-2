from datetime import datetime

from pydantic import Field

from app.schemas.common import ORMBaseSchema


class PropertyCreate(ORMBaseSchema):
    name: str = Field(..., min_length=1, max_length=255)
    property_type: str = Field(..., min_length=1, max_length=100)
    star_rating: int = Field(..., ge=0, le=7)


class PropertyRead(ORMBaseSchema):
    property_id: int
    name: str
    property_type: str
    star_rating: int
    created_at: datetime
    updated_at: datetime
