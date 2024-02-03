from typing import Optional

from pydantic import BaseModel

from src.submenu.schemas import SubmenuSchema


class MenuSchema(BaseModel):
    id: str
    title: str
    description: str
    submenus_count: int
    dishes_count: int
    submenus: list[SubmenuSchema]

    class Config:
        from_attributes = True


class CreateMenuSchema(BaseModel):
    title: str
    description: str


class UpdateMenuSchema(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
