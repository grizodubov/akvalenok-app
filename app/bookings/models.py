from datetime import date, datetime
from typing import Optional

from sqlalchemy import ForeignKey, Computed
from sqlalchemy.orm import relationship, mapped_column, Mapped

from app.database import Base


class Bookings(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    pool_id: Mapped[int] = mapped_column(ForeignKey("pools.id"))
    time_from: Mapped[datetime] = mapped_column(nullable=False)
    time_to: Mapped[datetime] = mapped_column(nullable=False)
    price: Mapped[int] = mapped_column(nullable=False)
    total_cost: Mapped[int] = mapped_column(Computed("(time_to - time_from) * price"))
    total_days: Mapped[int] = mapped_column(Computed("time_to - time_from"))
    created_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.now())
    updated_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.now())
    deleted_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)

    user: Mapped["User"] = relationship(uselist=False, lazy="selectin")
    pool: Mapped["Pools"] = relationship(back_populates="booking")

    def __str__(self):
        return f"Занятия #{self.id}"
