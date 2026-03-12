from enum import Enum

from sqlalchemy import BigInteger, Enum as SqlEnum, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base


class RoomStatusEnum(str, Enum):
    VACANT = "vacant"
    OCCUPIED = "occupied"
    OUT_OF_ORDER = "out_of_order"


class Room(Base):
    __tablename__ = "room"
    __table_args__ = (UniqueConstraint("property_id", "room_number", name="uq_room_property_room_number"),)

    room_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    property_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("property.property_id", ondelete="CASCADE"), index=True
    )
    building_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    room_type_id: Mapped[int] = mapped_column(BigInteger, index=True)
    room_number: Mapped[str] = mapped_column(String(50))
    floor: Mapped[str | None] = mapped_column(String(50), nullable=True)
    room_status: Mapped[RoomStatusEnum] = mapped_column(SqlEnum(RoomStatusEnum, name="room_status_enum"))

    property = relationship("Property", back_populates="rooms")
