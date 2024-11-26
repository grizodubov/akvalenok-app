import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class SBooking(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: uuid.UUID
    pool_id: int

    start_datetime: datetime
    end_datetime: datetime
    lesson_duration_minutes: int
    lessons_in_a_row: int
    price: float
    total_cost: float

    deleted_at: Optional[datetime]

class SBookingInfo(SBooking):
    model_config = ConfigDict(from_attributes=True)
    image_id: Optional[int]
    name: str
    description: Optional[str]
    services: list[str]

class SNewBooking(BaseModel):
    pool_id: int
    start_datetime: datetime
    end_datetime: datetime
    lessons_in_a_row: int = 1
