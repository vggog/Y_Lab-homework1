from uuid import uuid4

from sqlalchemy import select, func, and_
from sqlalchemy.orm import Mapped, relationship, mapped_column, column_property

from src.core.model import BaseModel
from src.submenu.model import SubmenuModel
from src.dish.model import DishModel


class MenuModel(BaseModel):
    __tablename__ = "menu"
    id: Mapped[str] = mapped_column(
        primary_key=True,
        default=lambda: str(uuid4()),
    )

    submenus: Mapped[list["SubmenuModel"]] = relationship(
        back_populates="menu",
        cascade="all, delete",
        passive_deletes=True,
    )
    submenus_count: Mapped[int] = column_property(
        select(
            func.count(
                SubmenuModel.id
            )
        ).
        where(SubmenuModel.menu_id == id).
        scalar_subquery()
    )
    dishes_count: Mapped[int] = column_property(
        select(
            func.count(
                DishModel.id
            )
        ).
        join(SubmenuModel).
        where(
            and_(
                SubmenuModel.menu_id == id,
                SubmenuModel.id == DishModel.submenu_id
            )
        ).
        correlate_except(DishModel).
        scalar_subquery()
    )
