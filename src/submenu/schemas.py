from pydantic import BaseModel


class CreateSubmenuSchema(BaseModel):
    title: str
    description: str


class SubmenuSchema(CreateSubmenuSchema):
    id: str

    class Config:
        from_attributes = True
