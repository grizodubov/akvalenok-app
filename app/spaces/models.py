from sqlalchemy import JSON, Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Spaces(Base):
    __tablename__ = "spaces"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    services = Column(JSON)
    pools_quantity = Column(Integer, nullable=False)
    image_id = Column(Integer)

    pool = relationship("Pools", back_populates="space")

    def __str__(self):
        return f"Помещение {self.name} {self.location[:30]}"
