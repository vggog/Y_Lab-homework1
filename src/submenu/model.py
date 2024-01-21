from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.model import BaseModel
from src.dish.model import DishModel


class SubmenuModel(BaseModel):
    __tablename__ = "submenu"

    menu_id: Mapped[str] = mapped_column(ForeignKey("menu.id"))
    dishes: Mapped[list["DishModel"]] = relationship(
        cascade="all, delete"
    )
