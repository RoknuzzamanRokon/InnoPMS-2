from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from models.inventory import RoomInventory
from schemas.booking import (
    BlockRoomsRequest,
    BookingRequest,
    BookingResponse,
    DemoBookingRequest,
    ReleaseBlockedRoomsRequest,
)
from services.inventory_service import calculate_available_rooms


def _load_inventory_rows_for_update(db: Session, property_id: int, room_type_id: int, start_date, end_date) -> list[RoomInventory]:
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
            .with_for_update()
        ).all()
    )


def _ensure_full_range(rows: list[RoomInventory], start_date, end_date) -> None:
    if len(rows) != (end_date - start_date).days:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inventory rows are missing for one or more requested dates",
        )


def book_rooms(db: Session, payload: BookingRequest) -> BookingResponse:
    try:
        rows = _load_inventory_rows_for_update(db, payload.property_id, payload.room_type_id, payload.start_date, payload.end_date)
        _ensure_full_range(rows, payload.start_date, payload.end_date)

        for row in rows:
            if row.available_rooms < payload.rooms_to_book:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Insufficient available rooms for {row.inventory_date.isoformat()}",
                )

        # Validate the whole stay first so partial updates cannot happen.
        for row in rows:
            row.booked_rooms += payload.rooms_to_book
            row.available_rooms = calculate_available_rooms(row.total_rooms, row.booked_rooms, row.blocked_rooms)

        db.commit()
        return BookingResponse(message="Rooms booked successfully", inventory=rows)
    except HTTPException:
        db.rollback()
        raise
    except Exception:
        db.rollback()
        raise


def block_rooms(db: Session, payload: BlockRoomsRequest) -> BookingResponse:
    try:
        rows = _load_inventory_rows_for_update(db, payload.property_id, payload.room_type_id, payload.start_date, payload.end_date)
        _ensure_full_range(rows, payload.start_date, payload.end_date)

        for row in rows:
            if row.available_rooms < payload.qty:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Insufficient available rooms to block for {row.inventory_date.isoformat()}",
                )

        for row in rows:
            row.blocked_rooms += payload.qty
            row.available_rooms = calculate_available_rooms(row.total_rooms, row.booked_rooms, row.blocked_rooms)

        db.commit()
        return BookingResponse(message="Rooms blocked successfully", inventory=rows)
    except HTTPException:
        db.rollback()
        raise
    except Exception:
        db.rollback()
        raise


def release_blocked_rooms(db: Session, payload: ReleaseBlockedRoomsRequest) -> BookingResponse:
    try:
        rows = _load_inventory_rows_for_update(db, payload.property_id, payload.room_type_id, payload.start_date, payload.end_date)
        _ensure_full_range(rows, payload.start_date, payload.end_date)

        for row in rows:
            if row.blocked_rooms < payload.qty:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Cannot release more blocked rooms than exist for {row.inventory_date.isoformat()}",
                )

        for row in rows:
            row.blocked_rooms -= payload.qty
            row.available_rooms = calculate_available_rooms(row.total_rooms, row.booked_rooms, row.blocked_rooms)

        db.commit()
        return BookingResponse(message="Blocked rooms released successfully", inventory=rows)
    except HTTPException:
        db.rollback()
        raise
    except Exception:
        db.rollback()
        raise


def demo_book_two_rooms(db: Session, payload: DemoBookingRequest) -> BookingResponse:
    request = BookingRequest(
        property_id=payload.property_id,
        room_type_id=payload.room_type_id,
        start_date=payload.start_date,
        end_date=payload.end_date,
        rooms_to_book=2,
    )
    return book_rooms(db, request)
