from sqlalchemy import Result, Select, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.core.repository import BaseRepository
from src.dish.model import DishModel


class Repository(BaseRepository):
    _model = DishModel

    async def get_by_id(
            self,
            async_session: async_sessionmaker[AsyncSession],
            object_id: str
    ) -> DishModel | None:
        """Получить по блюдо по id"""
        stmt: Select = select(self._model).where(self._model.id == object_id)

        async with async_session() as session:
            res: Result = await session.execute(stmt)

        return res.scalars().first()
