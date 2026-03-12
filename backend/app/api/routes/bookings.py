from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from api.deps import get_db
from schemas.booking import (
    BlockRoomsRequest,
    BookingRequest,
    BookingResponse,
    DemoBookingRequest,
    ReleaseBlockedRoomsRequest,
)
from services.booking_service import block_rooms, book_rooms, demo_book_two_rooms, release_blocked_rooms

router = APIRouter()


@router.post("/book", response_model=BookingResponse, status_code=status.HTTP_200_OK)
def book_rooms_endpoint(payload: BookingRequest, db: Session = Depends(get_db)) -> BookingResponse:
    return book_rooms(db, payload)


@router.post("/block", response_model=BookingResponse, status_code=status.HTTP_200_OK)
def block_rooms_endpoint(payload: BlockRoomsRequest, db: Session = Depends(get_db)) -> BookingResponse:
    return block_rooms(db, payload)


@router.post("/release-block", response_model=BookingResponse, status_code=status.HTTP_200_OK)
def release_blocked_rooms_endpoint(
    payload: ReleaseBlockedRoomsRequest, db: Session = Depends(get_db)
) -> BookingResponse:
    return release_blocked_rooms(db, payload)


@router.post("/demo/book-2", response_model=BookingResponse, status_code=status.HTTP_200_OK)
def demo_book_two_rooms_endpoint(payload: DemoBookingRequest, db: Session = Depends(get_db)) -> BookingResponse:
    return demo_book_two_rooms(db, payload)
