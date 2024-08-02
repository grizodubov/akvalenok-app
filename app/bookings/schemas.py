from datetime import date

from pydantic import BaseModel, ConfigDict


class SBooking(BaseModel):
    model_config = ConfigDict(from_attributes=True) # Pydantic v2
    id: int
    pool_id: int
    user_id: int
    time_from: date
    time_to: date
    price: int
    total_cost: int
    total_days: int
