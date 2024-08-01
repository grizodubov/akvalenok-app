from sqlalchemy import JSON, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, mapped_column, Mapped

from app.bookings.models import Bookings
from app.database import Base
from app.spaces.models import Spaces


class Pools(Base):
    __tablename__ = "pools"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    # space_id = mapped_column(Integer, ForeignKey("spaces.id"), nullable=False)
    space_id: Mapped[int] = mapped_column(Integer, ForeignKey("spaces.id"), nullable=False)
    name = mapped_column(String)
    description = mapped_column(String)
    price = mapped_column(Integer, nullable=False)
    services = mapped_column(JSON)
    quantity = mapped_column(Integer, nullable=False)
    image_id = mapped_column(Integer)

    space: Mapped["Spaces"] = relationship(back_populates="pool")
    booking: Mapped["Bookings"] = relationship(back_populates="pool")

    def __str__(self):
        return f"Бассейн {self.name}"
