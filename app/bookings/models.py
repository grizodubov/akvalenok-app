import uuid
from datetime import datetime, timezone, date
from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey, Computed, Integer, Date, Boolean, TIMESTAMP
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

    time_from: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False)
    price: Mapped[int] = mapped_column(nullable=False)
    total_cost: Mapped[int] = mapped_column(Computed("(date_to - date_from) * price"))

    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), default=datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=True, onupdate=datetime.now(timezone.utc))
    deleted_at: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP(timezone=True), nullable=True)

    user: Mapped["Users"] = relationship(back_populates="booking")
    pool: Mapped["Pools"] = relationship(back_populates="booking")

    def __str__(self):
        return f"Занятия #{self.id}"
