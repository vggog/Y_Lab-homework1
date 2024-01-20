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
