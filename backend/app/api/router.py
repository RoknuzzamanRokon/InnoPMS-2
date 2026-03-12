from fastapi import APIRouter

from api.routes import bookings, inventory, properties, rate_plans, rooms

api_router = APIRouter()
api_router.include_router(properties.router, prefix="/properties", tags=["properties"])
api_router.include_router(rooms.router, prefix="/rooms", tags=["rooms"])
api_router.include_router(rate_plans.router, prefix="/rate-plans", tags=["rate-plans"])
api_router.include_router(inventory.router, prefix="/inventory", tags=["inventory"])
api_router.include_router(bookings.router, prefix="/bookings", tags=["bookings"])
