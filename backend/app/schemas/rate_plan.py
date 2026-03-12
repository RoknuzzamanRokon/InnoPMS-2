from datetime import date
from decimal import Decimal

from pydantic import Field, model_validator

from app.models.rate_plan import ApplyToEnum
from app.schemas.common import ORMBaseSchema


class RatePlanCreate(ORMBaseSchema):
    property_id: int = Field(..., gt=0)
    start_date: date
    end_date: date
    base_rate: Decimal = Field(..., gt=0)
    currency: str = Field(..., min_length=3, max_length=10)
    apply_to: ApplyToEnum

    @model_validator(mode="after")
    def validate_dates(self) -> "RatePlanCreate":
        if self.end_date < self.start_date:
            raise ValueError("end_date must be on or after start_date")
        return self


class RatePlanRead(ORMBaseSchema):
    rate_plan_id: int
    property_id: int
    start_date: date
    end_date: date
    base_rate: Decimal
    currency: str
    apply_to: ApplyToEnum
