from datetime import date

from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Mapped


class SBooking(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    pool_id: int
    user_id: int
    time_from: date
    time_to: date
    price: int
    total_cost: int
    total_half_hours: int


class SNewBooking(BaseModel):
    pool_id: int
    time_from: date
    time_to: date
