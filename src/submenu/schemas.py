from typing import Optional

from pydantic import BaseModel

from src.dish.schemas import DishSchema


class CreateSubmenuSchema(BaseModel):
    title: str
    description: str


class SubmenuSchema(CreateSubmenuSchema):
    id: str
    dishes_count: int
    dishes: list[DishSchema]

    class Config:
        from_attributes = True


class UpdateSubmenuSchema(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
