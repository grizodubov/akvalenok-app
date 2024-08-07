from datetime import date

from pydantic import BaseModel, ConfigDict


class SBooking(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    pool_id: int
    user_id: int
    date_from: date
    date_to: date
    price: int
    total_cost: int
    total_days: int


class SNewBooking(BaseModel):
    pool_id: int
    date_from: date
    date_to: date
