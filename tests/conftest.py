import pytest
from fastapi.testclient import TestClient
from sqlalchemy.engine import create_engine

from src.core.model import BaseModel
from src.factory import AppFactory
from src.core.config import db_config


@pytest.fixture(autouse=True, scope="session")
def prepare_db():
    engine = create_engine(db_config.alchemy_url)
    BaseModel.metadata.create_all(engine)
    yield
    BaseModel.metadata.drop_all(engine)


client = TestClient(AppFactory.create_app())
