from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from .model import BaseModel
from .config import db_config


class BaseRepository:
    _model: BaseModel = NotImplemented
    engine = create_engine(db_config.alchemy_url)

    def get_all(self) -> list[_model]:
        with Session(self.engine) as session:
            return session.query(self._model).all()
