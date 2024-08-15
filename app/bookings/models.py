from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import ForeignKey, Computed, Integer, TIMESTAMP
from sqlalchemy.orm import relationship, mapped_column, Mapped

from app.database import Base


class Bookings(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    pool_id: Mapped[int] = mapped_column(ForeignKey("pools.id"))
    time_from: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False)
    time_to: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False)
    price: Mapped[int] = mapped_column(nullable=False)
    total_cost_rounded: Mapped[int] = mapped_column(Integer, Computed("ROUND(EXTRACT(EPOCH FROM (time_to - time_from)) / 1800) * "
                                                              "price"))
    total_half_hours_rounded: Mapped[int] = mapped_column(Integer, Computed("ROUND(EXTRACT(EPOCH FROM (time_to - time_from)) / 1800)"
                                                                    ))
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False, default=datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=True, onupdate=datetime.now(timezone.utc))
    deleted_at: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP(timezone=True), nullable=True)

    user: Mapped["Users"] = relationship(uselist=False, lazy="selectin")
    pool: Mapped["Pools"] = relationship(back_populates="booking")

    def __str__(self):
        return f"Занятия #{self.id}"
