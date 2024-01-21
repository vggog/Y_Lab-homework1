from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.core.model import BaseModel


class SubmenuModel(BaseModel):
    __tablename__ = "submenu"

    menu_id: Mapped[str] = mapped_column(ForeignKey("menu.id"))
