from datetime import date, timedelta

from pydantic import Field, model_validator

from schemas.common import ORMBaseSchema
from schemas.inventory import InventoryRead


class BookingRequest(ORMBaseSchema):
    property_id: int = Field(..., gt=0)
    room_type_id: int = Field(..., gt=0)
    start_date: date
    end_date: date
    rooms_to_book: int = Field(..., gt=0)

    @model_validator(mode="after")
    def validate_dates(self) -> "BookingRequest":
        if self.end_date <= self.start_date:
            raise ValueError("end_date must be after start_date")
        return self


class BlockRoomsRequest(ORMBaseSchema):
    property_id: int = Field(..., gt=0)
    room_type_id: int = Field(..., gt=0)
    start_date: date
    end_date: date
    qty: int = Field(..., gt=0)

    @model_validator(mode="after")
    def validate_dates(self) -> "BlockRoomsRequest":
        if self.end_date <= self.start_date:
            raise ValueError("end_date must be after start_date")
        return self


class ReleaseBlockedRoomsRequest(BlockRoomsRequest):
    pass


class BookingResponse(ORMBaseSchema):
    message: str
    inventory: list[InventoryRead]


class DemoBookingRequest(ORMBaseSchema):
    property_id: int = Field(..., gt=0)
    room_type_id: int = Field(..., gt=0)
    start_date: date
    nights: int = Field(default=3, ge=1, le=30)

    @property
    def end_date(self) -> date:
        return self.start_date + timedelta(days=self.nights)
