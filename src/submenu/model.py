from uuid import uuid4

from sqlalchemy import ForeignKey, select, func
from sqlalchemy.orm import Mapped, mapped_column, relationship, column_property

from src.core.model import BaseModel
from src.dish.model import DishModel


class SubmenuModel(BaseModel):
    __tablename__ = "submenu"

    id: Mapped[str] = mapped_column(
        primary_key=True,
        default=lambda: str(uuid4()),
    )

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
    dishes_count: Mapped[int] = column_property(
        select(
            func.count(
                DishModel.id
            )
        ).
        where(DishModel.submenu_id == id)
        .scalar_subquery()
    )
