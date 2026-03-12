from datetime import date, timedelta

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from models.inventory import RoomInventory
from models.property import Property
from models.room import Room
from schemas.room import BulkRoomCreate, BulkRoomDemoRequest, BulkRoomRead, RoomCreate
from services.inventory_service import calculate_available_rooms
from utils.dates import iter_dates


def _assert_property_exists(db: Session, property_id: int) -> None:
    if db.get(Property, property_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Property not found")


def _update_inventory_for_new_rooms(
    db: Session,
    *,
    property_id: int,
    room_type_id: int,
    qty: int,
    start_date: date,
    end_date: date,
) -> None:
    rows = list(
        db.scalars(
            select(RoomInventory)
            .where(
                RoomInventory.property_id == property_id,
                RoomInventory.room_type_id == room_type_id,
                RoomInventory.inventory_date >= start_date,
                RoomInventory.inventory_date < end_date,
            )
            .with_for_update()
        ).all()
    )
    rows_by_date = {row.inventory_date: row for row in rows}

    # Room insert and capacity update must succeed or fail together to keep stock accurate.
    for current_date in iter_dates(start_date, end_date):
        row = rows_by_date.get(current_date)
        if row is None:
            db.add(
                RoomInventory(
                    property_id=property_id,
                    room_type_id=room_type_id,
                    inventory_date=current_date,
                    total_rooms=qty,
                    booked_rooms=0,
                    blocked_rooms=0,
                    available_rooms=qty,
                )
            )
            continue

        row.total_rooms += qty
        row.available_rooms = calculate_available_rooms(row.total_rooms, row.booked_rooms, row.blocked_rooms)
        if row.available_rooms < 0:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Inventory for {current_date.isoformat()} would become negative",
            )


def create_room(db: Session, payload: RoomCreate) -> Room:
    try:
        _assert_property_exists(db, payload.property_id)
        inventory_start = payload.inventory_start_date or date.today()
        inventory_end = payload.inventory_end_date or (inventory_start + timedelta(days=1))

        room = Room(
            property_id=payload.property_id,
            building_id=payload.building_id,
            room_type_id=payload.room_type_id,
            room_number=payload.room_number,
            floor=payload.floor,
            room_status=payload.room_status,
        )

        db.add(room)
        db.flush()
        _update_inventory_for_new_rooms(
            db,
            property_id=payload.property_id,
            room_type_id=payload.room_type_id,
            qty=1,
            start_date=inventory_start,
            end_date=inventory_end,
        )
        db.commit()
        db.refresh(room)
        return room
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Room number already exists") from exc
    except HTTPException:
        db.rollback()
        raise
    except Exception:
        db.rollback()
        raise


def bulk_create_rooms(db: Session, payload: BulkRoomCreate) -> BulkRoomRead:
    try:
        _assert_property_exists(db, payload.property_id)
        inventory_start = payload.inventory_start_date or date.today()
        inventory_end = payload.inventory_end_date or (inventory_start + timedelta(days=1))

        rooms = [
            Room(
                property_id=payload.property_id,
                building_id=payload.building_id,
                room_type_id=payload.room_type_id,
                room_number=room_number,
                floor=payload.floor,
                room_status=payload.room_status,
            )
            for room_number in payload.room_numbers
        ]

        db.add_all(rooms)
        db.flush()
        _update_inventory_for_new_rooms(
            db,
            property_id=payload.property_id,
            room_type_id=payload.room_type_id,
            qty=len(rooms),
            start_date=inventory_start,
            end_date=inventory_end,
        )
        db.commit()
        for room in rooms:
            db.refresh(room)
        return BulkRoomRead(created_count=len(rooms), rooms=rooms)
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="One or more room_numbers already exist for this property",
        ) from exc
    except HTTPException:
        db.rollback()
        raise
    except Exception:
        db.rollback()
        raise


def demo_create_ten_rooms(db: Session, payload: BulkRoomDemoRequest) -> BulkRoomRead:
    room_numbers = [str(payload.start_room_number + offset) for offset in range(10)]
    request = BulkRoomCreate(
        property_id=payload.property_id,
        building_id=payload.building_id,
        room_type_id=payload.room_type_id,
        floor=payload.floor,
        room_status=payload.room_status,
        room_numbers=room_numbers,
        inventory_start_date=payload.inventory_start_date,
        inventory_end_date=payload.inventory_end_date,
    )
    return bulk_create_rooms(db, request)
