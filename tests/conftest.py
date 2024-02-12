import asyncio

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine

from main import app
from src.core.config import load_db_config
from src.core.model import BaseModel

engine = create_async_engine(load_db_config().alchemy_url)


@pytest.fixture(scope='session')
def event_loop(request):
    """Создает экземпляр стандартного цикла событий
    для каждого тестового случая."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(autouse=True, scope='session')
async def prepare_db():
    async with engine.begin() as connection:
        await connection.run_sync(BaseModel.metadata.create_all)

    yield

    async with engine.begin() as connection:
        await connection.run_sync(BaseModel.metadata.drop_all)


sync_client = TestClient(app=app, base_url='http://test')


@pytest_asyncio.fixture(scope='session')
async def client():
    """Асинхронный клиент."""
    async with AsyncClient(app=app, base_url='http://test') as client:
        yield client
