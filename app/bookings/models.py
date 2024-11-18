import uuid
from datetime import datetime, timezone, date
from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey, Computed, Integer, DateTime, Float
from sqlalchemy.orm import relationship, mapped_column, Mapped

from app.database import Base

if TYPE_CHECKING:
    from app.users.models import Users
    from app.spaces.pools.models import Pools


class Bookings(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    pool_id: Mapped[int] = mapped_column(ForeignKey("pools.id"))

    start_datetime: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    bookings_in_a_row: Mapped[int] = mapped_column(Integer, nullable=False)
    lesson_duration_minutes: Mapped[int] = mapped_column(Integer, default=30, nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    total_cost: Mapped[float] = mapped_column(Computed("bookings_in_a_row * price"))
    end_datetime: Mapped[datetime] = mapped_column(Computed("start_datetime + timedelta(minutes=bookings_in_a_row * lesson_duration_minutes)"))

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), onupdate=datetime.now(timezone.utc), nullable=True)
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    user: Mapped["Users"] = relationship(back_populates="booking")
    pool: Mapped["Pools"] = relationship(back_populates="booking")

    def __str__(self):
        return f"Занятия #{self.id}"
