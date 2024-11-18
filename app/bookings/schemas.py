import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class SBooking(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: uuid.UUID
    pool_id: int
    start_datetime: datetime
    bookings_in_a_row: int
    price: float

class SNewBooking(BaseModel):
    pool_id: int
    start_datetime: datetime
    bookings_in_a_row : int
