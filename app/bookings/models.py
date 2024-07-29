from typing import List

from sqlalchemy import Computed, Date, ForeignKey, Integer
from sqlalchemy.orm import relationship, mapped_column, Mapped

from app.database import Base


class Bookings(Base):
    __tablename__ = "bookings"

    id = mapped_column(Integer, primary_key=True)
    pool_id = mapped_column(Integer, ForeignKey("rooms.id"))
    user_id = mapped_column(Integer, ForeignKey("users.id"))
    time_from = mapped_column(Date, nullable=False)
    time_to = mapped_column(Date, nullable=False)
    price = mapped_column(Integer, nullable=False)
    total_cost = mapped_column(Integer, Computed("(date_to - date_from) * price"))
    total_days = mapped_column(Integer, Computed("date_to - date_from"))

    # user = relationship("Users", back_populates="booking")
    user: Mapped[List["Users"]] = relationship(back_populates="booking")
    # pool = relationship("Pools", back_populates="booking")
    pool: Mapped[List["Pools"]] = relationship(back_populates="booking")

    def __str__(self):
        return f"Занятия #{self.id}"
