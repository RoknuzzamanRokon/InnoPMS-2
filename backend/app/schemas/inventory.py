from datetime import date, datetime, timedelta

from pydantic import Field, model_validator

from schemas.common import ORMBaseSchema


class InventoryInitializeRequest(ORMBaseSchema):
    property_id: int = Field(..., gt=0)
    room_type_id: int = Field(..., gt=0)
    start_date: date
    end_date: date

    @model_validator(mode="after")
    def validate_dates(self) -> "InventoryInitializeRequest":
        if self.end_date <= self.start_date:
            raise ValueError("end_date must be after start_date")
        return self


class InventoryRead(ORMBaseSchema):
    inventory_id: int
    property_id: int
    room_type_id: int
    inventory_date: date
    total_rooms: int
    available_rooms: int
    booked_rooms: int
    blocked_rooms: int
    updated_at: datetime


class InventoryInitializeDemoRequest(ORMBaseSchema):
    property_id: int = Field(..., gt=0)
    room_type_id: int = Field(..., gt=0)
    start_date: date | None = None
    days: int = Field(default=7, ge=1, le=365)

    @property
    def resolved_start_date(self) -> date:
        return self.start_date or date.today()

    @property
    def resolved_end_date(self) -> date:
        return self.resolved_start_date + timedelta(days=self.days)
