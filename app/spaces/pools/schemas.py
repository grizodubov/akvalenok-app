from typing import Optional

from pydantic import BaseModel, ConfigDict


class SPool(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    space_id: int
    name: str
    description: Optional[str]
    services: list[str]
    price: int
    quantity: int
    image_id: int


class SPoolInfo(SPool):
    model_config = ConfigDict(from_attributes=True)

    total_cost: int
    pools_left: int
