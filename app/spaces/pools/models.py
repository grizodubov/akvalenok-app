from sqlalchemy import JSON, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Pools(Base):
    __tablename__ = "pools"

    id = Column(Integer, primary_key=True, nullable=False)
    space_id = Column(Integer, ForeignKey("spaces.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Integer, nullable=False)
    services = Column(JSON, nullable=True)
    quantity = Column(Integer, nullable=False)
    image_id = Column(Integer)

    space = relationship("Spaces", back_populates="room")
    booking = relationship("Bookings", back_populates="room")

    def __str__(self):
        return f"Бассеин {self.name}"
