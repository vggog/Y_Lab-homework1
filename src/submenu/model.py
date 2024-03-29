from uuid import uuid4

from sqlalchemy import ForeignKey, func, select
from sqlalchemy.orm import Mapped, column_property, mapped_column, relationship

from src.core.model import BaseModel
from src.dish.model import DishModel


class SubmenuModel(BaseModel):
    __tablename__ = 'submenu'

    id: Mapped[str] = mapped_column(
        primary_key=True,
        default=lambda: str(uuid4()),
    )

    menu_id: Mapped[str] = mapped_column(
        ForeignKey(
            'menu.id',
            ondelete='CASCADE',
        )
    )
    menu = relationship(
        'MenuModel',
        back_populates='submenus',
    )
    dishes: Mapped[list['DishModel']] = relationship(
        back_populates='submenu',
        cascade='all, delete',
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
