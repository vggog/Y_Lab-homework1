from pydantic import BaseModel


class SubmenuSchema(BaseModel):
    id: str
    title: str
    description: str

    class Config:
        from_attributes = True
