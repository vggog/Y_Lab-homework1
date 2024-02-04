from pydantic import BaseModel

from src.submenu.schemas import SubmenuSchema


class CreateMenuSchema(BaseModel):
    title: str
    description: str


class MenuSchema(CreateMenuSchema):
    id: str
    submenus_count: int
    dishes_count: int
    submenus: list[SubmenuSchema]

    class Config:
        from_attributes = True


class UpdateMenuSchema(BaseModel):
    title: str | None = None
    description: str | None = None
