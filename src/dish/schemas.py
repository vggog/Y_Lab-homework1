from typing import Optional

from pydantic import BaseModel


class CreateDishSchema(BaseModel):
    price: str
    title: str
    description: str


class DishSchema(CreateDishSchema):
    id: str

    class Config:
        from_attributes = True


class UpdateDishSchema(BaseModel):
    price: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
