from datetime import date

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from api.deps import get_db
from schemas.inventory import (
    InventoryInitializeDemoRequest,
    InventoryInitializeRequest,
    InventoryRead,
)
from services.inventory_service import get_inventory, initialize_inventory, initialize_inventory_demo

router = APIRouter()


@router.post("/initialize", response_model=list[InventoryRead], status_code=status.HTTP_201_CREATED)
def initialize_inventory_endpoint(
    payload: InventoryInitializeRequest, db: Session = Depends(get_db)
) -> list[InventoryRead]:
    return initialize_inventory(db, payload)


@router.get("", response_model=list[InventoryRead])
def get_inventory_endpoint(
    property_id: int = Query(..., gt=0),
    room_type_id: int = Query(..., gt=0),
    start_date: date = Query(...),
    end_date: date = Query(...),
    db: Session = Depends(get_db),
) -> list[InventoryRead]:
    return get_inventory(
        db,
        property_id=property_id,
        room_type_id=room_type_id,
        start_date=start_date,
        end_date=end_date,
    )


@router.post("/demo/initialize", response_model=list[InventoryRead], status_code=status.HTTP_201_CREATED)
def initialize_inventory_demo_endpoint(
    payload: InventoryInitializeDemoRequest, db: Session = Depends(get_db)
) -> list[InventoryRead]:
    return initialize_inventory_demo(db, payload)
