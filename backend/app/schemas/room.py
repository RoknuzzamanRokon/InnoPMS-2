from datetime import date

from pydantic import Field, model_validator

from app.models.room import RoomStatusEnum
from app.schemas.common import ORMBaseSchema


class RoomCreate(ORMBaseSchema):
    property_id: int = Field(..., gt=0)
    building_id: int | None = Field(default=None, gt=0)
    room_type_id: int = Field(..., gt=0)
    room_number: str = Field(..., min_length=1, max_length=50)
    floor: str | None = Field(default=None, max_length=50)
    room_status: RoomStatusEnum
    inventory_start_date: date | None = None
    inventory_end_date: date | None = None

    @model_validator(mode="after")
    def validate_inventory_range(self) -> "RoomCreate":
        if (self.inventory_start_date is None) != (self.inventory_end_date is None):
            raise ValueError("inventory_start_date and inventory_end_date must be provided together")
        if self.inventory_start_date and self.inventory_end_date and self.inventory_end_date <= self.inventory_start_date:
            raise ValueError("inventory_end_date must be after inventory_start_date")
        return self


class RoomRead(ORMBaseSchema):
    room_id: int
    property_id: int
    building_id: int | None
    room_type_id: int
    room_number: str
    floor: str | None
    room_status: RoomStatusEnum


class BulkRoomCreate(ORMBaseSchema):
    property_id: int = Field(..., gt=0)
    building_id: int | None = Field(default=None, gt=0)
    room_type_id: int = Field(..., gt=0)
    floor: str | None = Field(default=None, max_length=50)
    room_status: RoomStatusEnum
    room_numbers: list[str] = Field(..., min_length=1)
    inventory_start_date: date | None = None
    inventory_end_date: date | None = None

    @model_validator(mode="after")
    def validate_payload(self) -> "BulkRoomCreate":
        if len(set(self.room_numbers)) != len(self.room_numbers):
            raise ValueError("room_numbers must be unique within the request")
        if (self.inventory_start_date is None) != (self.inventory_end_date is None):
            raise ValueError("inventory_start_date and inventory_end_date must be provided together")
        if self.inventory_start_date and self.inventory_end_date and self.inventory_end_date <= self.inventory_start_date:
            raise ValueError("inventory_end_date must be after inventory_start_date")
        return self


class BulkRoomRead(ORMBaseSchema):
    created_count: int
    rooms: list[RoomRead]


class BulkRoomDemoRequest(ORMBaseSchema):
    property_id: int = Field(..., gt=0)
    room_type_id: int = Field(..., gt=0)
    building_id: int | None = Field(default=None, gt=0)
    floor: str | None = Field(default="1", max_length=50)
    room_status: RoomStatusEnum = RoomStatusEnum.VACANT
    start_room_number: int = Field(default=101, ge=1)
    inventory_start_date: date | None = None
    inventory_end_date: date | None = None
