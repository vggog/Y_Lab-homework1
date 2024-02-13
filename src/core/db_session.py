from typing import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.core.config import db_config


async def get_db_session() -> AsyncIterator[async_sessionmaker[AsyncSession]]:
    """
    Функция для получения асинхронной сессии подключения к бд.
    :return:
    """
    engine = create_async_engine(db_config.alchemy_url)
    session = async_sessionmaker(
        engine,
        expire_on_commit=False
    )

    yield session
