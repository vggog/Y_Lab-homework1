from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.model import BaseModel
from src.dish.model import DishModel


class SubmenuModel(BaseModel):
    __tablename__ = "submenu"

    menu_id: Mapped[str] = mapped_column(
        ForeignKey(
            "menu.id",
            ondelete="CASCADE",
        )
    )
    menu: Mapped["MenuModel"] = relationship(
        back_populates="submenus",
    )
    dishes: Mapped[list["DishModel"]] = relationship(
        back_populates="submenu",
        cascade="all, delete",
        passive_deletes=True,
    )
    dishes_count: Mapped[int] = mapped_column(
        default=0,
    )
