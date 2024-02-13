from typing import Sequence

from sqlalchemy import Result, Select, delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.sql.dml import Delete, ReturningUpdate

from src.core.model import BaseModel


class BaseRepository:
    _model: type[BaseModel] = NotImplemented

    async def get_all(
            self,
            async_session: async_sessionmaker[AsyncSession],
            **filters
    ) -> Sequence[BaseModel]:
        stmt: Select = select(self._model).filter_by(**filters)
        async with async_session() as session:
            res = await session.execute(stmt)

        return res.scalars().all()

    async def get(
            self,
            async_session: async_sessionmaker[AsyncSession],
            **filters
    ) -> BaseModel | None:
        stmt: Select = select(self._model).filter_by(**filters)

        async with async_session() as session:
            res = await session.execute(stmt)

        return res.scalars().first()

    async def create(
            self,
            async_session: async_sessionmaker[AsyncSession],
            **kwargs
    ) -> BaseModel:
        created_object: BaseModel = self._model(**kwargs)

        async with async_session() as session:
            session.add(created_object)
            await session.commit()
            await session.refresh(created_object)

        return created_object

    async def update(
            self,
            object_id: str,
            async_session: async_sessionmaker[AsyncSession],
            **kwargs
    ) -> BaseModel | None:
        stmt: ReturningUpdate = (
            update(self._model).
            where(self._model.id == object_id).
            values(**kwargs).returning()
        )

        async with async_session() as session:
            await session.execute(stmt)
            await session.commit()

            res: Result = await session.execute(
                select(self._model).where(self._model.id == object_id)
            )

        return res.scalars().first()

    async def delete(
            self,
            object_id: str,
            async_session: async_sessionmaker[AsyncSession],
    ) -> None:
        stmt: Delete = (
            delete(self._model).
            where(self._model.id == object_id)
        )

        async with async_session() as session:
            await session.execute(stmt)
            await session.commit()
