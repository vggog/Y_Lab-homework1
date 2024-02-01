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
    price: str | None = None
    title: str | None = None
    description: str | None = None
