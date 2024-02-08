from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.core.repository import BaseRepository
from src.dish.model import DishModel
from src.menu.model import MenuModel
from src.submenu.model import SubmenuModel


class Repository(BaseRepository):
    _model = MenuModel

    async def get_all_dishes(
            self,
            menu_id: str,
            async_session: async_sessionmaker[AsyncSession],
    ) -> Sequence[DishModel]:
        """Метод для получения всех блюд, принадлежащих меню"""
        stmt = select(DishModel).filter(
            MenuModel.id == SubmenuModel.menu_id
        ).filter(
            SubmenuModel.id == DishModel.submenu_id
        ).filter(
            MenuModel.id == menu_id
        )

        async with async_session() as session:
            res = await session.execute(stmt)

        return res.scalars().all()

        #
        # with Session(self.engine) as session:
        #     return (
        #         session.query(
        #             DishModel
        #         ).filter(
        #             MenuModel.id == SubmenuModel.menu_id
        #         ).filter(
        #             SubmenuModel.id == DishModel.submenu_id
        #         ).filter(
        #             MenuModel.id == menu_id
        #         ).all()
        #     )
