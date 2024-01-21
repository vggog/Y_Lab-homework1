from sqlalchemy import create_engine, update, delete
from sqlalchemy.orm import Session

from .model import BaseModel
from .config import db_config


class BaseRepository:
    _model: BaseModel = NotImplemented
    engine = create_engine(db_config.alchemy_url)

    def get_all(self) -> list[_model]:
        with Session(self.engine) as session:
            return session.query(self._model).all()

    def get_by_id(self, object_id: str) -> _model:
        with Session(self.engine) as session:
            return session.query(self._model).filter_by(id=object_id).first()

    def get_all_by_filter(self, **kwargs) -> list[_model]:
        with Session(self.engine) as session:
            return session.query(self._model).filter_by(**kwargs).all()

    def create(self, **kwargs) -> _model:
        created_object = self._model(**kwargs)

        with Session(self.engine) as session:
            session.add(created_object)
            session.commit()
            session.refresh(created_object)

        return created_object

    def update(self, object_id: str, **kwargs) -> _model:
        stmt = (
            update(self._model).
            where(self._model.id == object_id).
            values(**kwargs).returning()
        )

        with Session(self.engine) as session:
            session.execute(stmt)
            session.commit()

            return session.query(self._model).filter_by(id=object_id).first()

    def delete(self, object_id: str):
        stmt = (
            delete(self._model).
            where(self._model.id == object_id)
        )

        with Session(self.engine) as session:
            session.execute(stmt)
            session.commit()
