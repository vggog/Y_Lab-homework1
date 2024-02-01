from uuid import uuid4

from sqlalchemy import and_, func, select
from sqlalchemy.orm import Mapped, column_property, mapped_column, relationship

from src.core.model import BaseModel
from src.dish.model import DishModel
from src.submenu.model import SubmenuModel


class MenuModel(BaseModel):
    __tablename__ = 'menu'
    id: Mapped[str] = mapped_column(
        primary_key=True,
        default=lambda: str(uuid4()),
    )

    submenus: Mapped[list['SubmenuModel']] = relationship(
        back_populates='menu',
        cascade='all, delete',
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
