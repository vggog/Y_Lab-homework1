from typing import Optional

from pydantic import BaseModel


class MenuSchema(BaseModel):
    id: int
    title: str
    description: str

    class Config:
        from_attributes = True


class CreateMenuSchema(BaseModel):
    title: str
    description: str


class UpdateMenuSchema(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
