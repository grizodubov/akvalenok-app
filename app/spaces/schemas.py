from pydantic import BaseModel, ConfigDict


class SSpace(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    location: str
    services: list[str]
    pools_quantity: int
    image_id: int
