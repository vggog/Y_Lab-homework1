from sqlalchemy.orm import Mapped

from src.core.model import BaseModel


class MenuModel(BaseModel):
    __tablename__ = "menu"

    title: Mapped[str]
    description: Mapped[str]
