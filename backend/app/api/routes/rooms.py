from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.room import BulkRoomCreate, BulkRoomDemoRequest, BulkRoomRead, RoomCreate, RoomRead
from app.services.room_service import bulk_create_rooms, create_room, demo_create_ten_rooms

router = APIRouter()


@router.post("", response_model=RoomRead, status_code=status.HTTP_201_CREATED)
def create_room_endpoint(payload: RoomCreate, db: Session = Depends(get_db)) -> RoomRead:
    return create_room(db, payload)


@router.post("/bulk", response_model=BulkRoomRead, status_code=status.HTTP_201_CREATED)
def bulk_create_rooms_endpoint(payload: BulkRoomCreate, db: Session = Depends(get_db)) -> BulkRoomRead:
    return bulk_create_rooms(db, payload)


@router.post("/demo/create-10", response_model=BulkRoomRead, status_code=status.HTTP_201_CREATED)
def demo_create_ten_rooms_endpoint(
    payload: BulkRoomDemoRequest, db: Session = Depends(get_db)
) -> BulkRoomRead:
    return demo_create_ten_rooms(db, payload)
