from sqlalchemy import create_engine, insert
from sqlalchemy.orm import Session

from .model import BaseModel
from .config import db_config


class BaseRepository:
    _model: BaseModel = NotImplemented
    engine = create_engine(db_config.alchemy_url)

    def get_all(self) -> list[_model]:
        with Session(self.engine) as session:
            return session.query(self._model).all()

    def get_by_id(self, object_id: int) -> _model:
        with Session(self.engine) as session:
            return session.query(self._model).filter_by(id=object_id).first()

    def create(self, **kwargs) -> _model:
        created_object = self._model(**kwargs)

        with Session(self.engine) as session:
            session.add(created_object)
            session.commit()
            session.refresh(created_object)

        return created_object
