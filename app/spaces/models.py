from typing import List

from sqlalchemy import JSON, Integer, String
from sqlalchemy.orm import relationship, mapped_column, Mapped

from app.database import Base


class Spaces(Base):
    __tablename__ = "spaces"

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    location = mapped_column(String, nullable=False)
    services = mapped_column(JSON)
    pools_quantity = mapped_column(Integer, nullable=False)
    image_id = mapped_column(Integer)

    # pool = relationship("Pools", back_populates="space")
    pools: Mapped[List["Pools"]] = relationship(back_populates="space")

    def __str__(self):
        return f"Помещение {self.name} {self.location[:30]}"
