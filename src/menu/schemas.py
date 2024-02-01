from pydantic import BaseModel


class MenuSchema(BaseModel):
    id: str
    title: str
    description: str
    submenus_count: int
    dishes_count: int

    class Config:
        from_attributes = True


class CreateMenuSchema(BaseModel):
    title: str
    description: str


class UpdateMenuSchema(BaseModel):
    title: str | None = None
    description: str | None = None
