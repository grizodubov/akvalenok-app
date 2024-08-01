from datetime import date

from pydantic import BaseModel, ConfigDict


class SBooking(BaseModel):
    model_config = ConfigDict(from_attributes=True) # Pydantic v2
    id: int
    time_from: date
    time_to: date
    price: int
    user_id: int
    pool_id: int
    created_at: date
    updated_at: date
    deleted_at: date
