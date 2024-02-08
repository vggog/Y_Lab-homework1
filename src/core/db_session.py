from typing import AsyncIterator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.core.config import load_db_config
from src.core.config.schemas import DBConfig


async def get_db_session(
        db_conf: DBConfig = Depends(load_db_config),
) -> AsyncIterator[async_sessionmaker[AsyncSession]]:
    """
    Функция для получения асинхронной сессии подключения к бд.
    :return:
    """
    engine = create_async_engine(db_conf.alchemy_url)
    session = async_sessionmaker(
        engine,
        expire_on_commit=False
    )

    yield session
