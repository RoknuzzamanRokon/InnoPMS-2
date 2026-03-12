from datetime import datetime

from sqlalchemy import DateTime, Integer, SmallInteger, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base_class import Base


class Property(Base):
    __tablename__ = "property"

    property_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255))
    property_type: Mapped[str] = mapped_column(String(100))
    star_rating: Mapped[int] = mapped_column(SmallInteger)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )

    rate_plans = relationship("RatePlan", back_populates="property", cascade="all, delete-orphan")
    rooms = relationship("Room", back_populates="property", cascade="all, delete-orphan")
    inventory_rows = relationship("RoomInventory", back_populates="property", cascade="all, delete-orphan")
