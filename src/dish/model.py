from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.core.model import BaseModel


class DishModel(BaseModel):
    __tablename__ = "dish"

    price: Mapped[str]
    submenu_id: Mapped[str] = mapped_column(ForeignKey("submenu.id"))
