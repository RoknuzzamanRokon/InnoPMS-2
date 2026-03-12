from datetime import date

from fastapi import HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.inventory import RoomInventory
from app.models.property import Property
from app.models.room import Room
from app.schemas.inventory import InventoryInitializeDemoRequest, InventoryInitializeRequest
from app.utils.dates import iter_dates


def calculate_available_rooms(total_rooms: int, booked_rooms: int, blocked_rooms: int) -> int:
    return total_rooms - booked_rooms - blocked_rooms


def _validate_property_exists(db: Session, property_id: int) -> None:
    if db.get(Property, property_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Property not found")


def get_inventory(
    db: Session, *, property_id: int, room_type_id: int, start_date: date, end_date: date
) -> list[RoomInventory]:
    if end_date <= start_date:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="end_date must be after start_date")

    return list(
        db.scalars(
            select(RoomInventory)
            .where(
                RoomInventory.property_id == property_id,
                RoomInventory.room_type_id == room_type_id,
                RoomInventory.inventory_date >= start_date,
                RoomInventory.inventory_date < end_date,
            )
            .order_by(RoomInventory.inventory_date)
        ).all()
    )


def initialize_inventory(db: Session, payload: InventoryInitializeRequest) -> list[RoomInventory]:
    try:
        _validate_property_exists(db, payload.property_id)

        room_count = db.scalar(
            select(func.count(Room.room_id)).where(
                Room.property_id == payload.property_id,
                Room.room_type_id == payload.room_type_id,
            )
        )
        room_count = int(room_count or 0)

        if room_count <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No rooms found for the given property_id and room_type_id",
            )

        rows = list(
            db.scalars(
                select(RoomInventory)
                .where(
                    RoomInventory.property_id == payload.property_id,
                    RoomInventory.room_type_id == payload.room_type_id,
                    RoomInventory.inventory_date >= payload.start_date,
                    RoomInventory.inventory_date < payload.end_date,
                )
                .with_for_update()
            ).all()
        )
        rows_by_date = {row.inventory_date: row for row in rows}

        for current_date in iter_dates(payload.start_date, payload.end_date):
            row = rows_by_date.get(current_date)
            if row is None:
                row = RoomInventory(
                    property_id=payload.property_id,
                    room_type_id=payload.room_type_id,
                    inventory_date=current_date,
                    total_rooms=room_count,
                    booked_rooms=0,
                    blocked_rooms=0,
                    available_rooms=room_count,
                )
                db.add(row)
                rows_by_date[current_date] = row
            else:
                row.total_rooms = room_count
                row.available_rooms = calculate_available_rooms(row.total_rooms, row.booked_rooms, row.blocked_rooms)
                if row.available_rooms < 0:
                    raise HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail=f"Inventory for {current_date.isoformat()} would become negative",
                    )

        db.commit()
        return [rows_by_date[current_date] for current_date in sorted(rows_by_date)]
    except HTTPException:
        db.rollback()
        raise
    except Exception:
        db.rollback()
        raise


def initialize_inventory_demo(db: Session, payload: InventoryInitializeDemoRequest) -> list[RoomInventory]:
    request = InventoryInitializeRequest(
        property_id=payload.property_id,
        room_type_id=payload.room_type_id,
        start_date=payload.resolved_start_date,
        end_date=payload.resolved_end_date,
    )
    return initialize_inventory(db, request)
