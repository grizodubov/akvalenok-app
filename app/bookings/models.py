import datetime
from typing import Optional

from sqlalchemy import ForeignKey, Computed
from sqlalchemy.orm import relationship, mapped_column, Mapped

from app.database import Base


class Bookings(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)

    time_from: Mapped[datetime.datetime] = mapped_column(nullable=False)
    time_to: Mapped[datetime.datetime] = mapped_column(nullable=False)
    price: Mapped[int] = mapped_column(nullable=False)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    user: Mapped["User"] = relationship(uselist=False, lazy="selectin")
    pool_id: Mapped[int] = mapped_column(ForeignKey("pools.id"))
    pool: Mapped["Pools"] = relationship(back_populates="booking")

    total_cost: Mapped[int] = mapped_column(Computed("(time_to - time_from) * price"))
    total_days: Mapped[int] = mapped_column(Computed("time_to - time_from"))

    created_at: Mapped[datetime.datetime] = mapped_column(nullable=False, default=datetime.datetime.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(nullable=False, default=datetime.datetime.now())
    deleted_at: Mapped[Optional[datetime.datetime]] = mapped_column(nullable=True)

    def __str__(self):
        return f"Занятия #{self.id}"
