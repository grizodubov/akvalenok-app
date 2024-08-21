import uuid
from datetime import datetime, date

from pydantic import BaseModel, ConfigDict


class SBooking(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: uuid.UUID
    pool_id: int
    date_from : date
    # time_from: datetime
    date_to : date
    # time_to: datetime
    price: int
    total_cost: int
    total_days : int
    # total_half_hours: int


class SNewBooking(BaseModel):
    pool_id: int
    date_from : date
    # time_from: datetime
    date_to: date
    # time_to: datetime
