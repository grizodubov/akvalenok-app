from datetime import datetime

from pydantic import BaseModel, ConfigDict


class SBooking(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    pool_id: int
    user_id: int
    time_from: datetime
    time_to: datetime
    price: int
    total_cost: int
    total_half_hours: int


class SNewBooking(BaseModel):
    pool_id: int
    time_from: datetime
    time_to: datetime
