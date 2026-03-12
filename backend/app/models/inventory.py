from datetime import date, datetime

from sqlalchemy import BigInteger, Date, DateTime, ForeignKey, SmallInteger, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base


class RoomInventory(Base):
    __tablename__ = "room_inventory"
    __table_args__ = (
        UniqueConstraint(
            "property_id", "room_type_id", "inventory_date", name="uq_room_inventory_property_room_type_date"
        ),
    )

    inventory_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    property_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("property.property_id", ondelete="CASCADE"), index=True
    )
    room_type_id: Mapped[int] = mapped_column(BigInteger, index=True)
    inventory_date: Mapped[date] = mapped_column(Date, index=True)
    total_rooms: Mapped[int] = mapped_column(SmallInteger)
    available_rooms: Mapped[int] = mapped_column(SmallInteger)
    booked_rooms: Mapped[int] = mapped_column(SmallInteger, default=0)
    blocked_rooms: Mapped[int] = mapped_column(SmallInteger, default=0)
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    property = relationship("Property", back_populates="inventory_rows")
