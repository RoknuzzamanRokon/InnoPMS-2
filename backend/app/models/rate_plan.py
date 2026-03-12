from datetime import date
from decimal import Decimal
from enum import Enum

from sqlalchemy import Date, Enum as SqlEnum, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base


class ApplyToEnum(str, Enum):
    PER_ROOM = "per_room"
    PER_PERSON = "per_person"
    PER_STAY = "per_stay"


class RatePlan(Base):
    __tablename__ = "rate_plan"

    rate_plan_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    property_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("property.property_id", ondelete="CASCADE"), index=True
    )
    start_date: Mapped[date] = mapped_column(Date)
    end_date: Mapped[date] = mapped_column(Date)
    base_rate: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    currency: Mapped[str] = mapped_column(String(10))
    apply_to: Mapped[ApplyToEnum] = mapped_column(SqlEnum(ApplyToEnum, name="apply_to_enum"))

    property = relationship("Property", back_populates="rate_plans")
