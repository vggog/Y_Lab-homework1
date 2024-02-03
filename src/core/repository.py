from sqlalchemy import create_engine, delete, update
from sqlalchemy.orm import Session

from .config import db_config
from .model import BaseModel


class BaseRepository:
    _model: type[BaseModel] = NotImplemented
    engine = create_engine(db_config.alchemy_url)

    def get_all(self) -> list[BaseModel]:
        with Session(self.engine) as session:
            return session.query(self._model).all()

    def get_by_id(self, object_id: str) -> BaseModel | None:
        with Session(self.engine) as session:
            return session.query(self._model).filter_by(id=object_id).first()

    def get(self, **kwargs) -> BaseModel | None:
        with Session(self.engine) as session:
            return session.query(self._model).filter_by(**kwargs).first()

    def get_all_by_filter(self, **kwargs) -> list[BaseModel]:
        with Session(self.engine) as session:
            return session.query(self._model).filter_by(**kwargs).all()

    def create(self, **kwargs) -> BaseModel:
        created_object = self._model(**kwargs)

        with Session(self.engine) as session:
            session.add(created_object)
            session.commit()
            session.refresh(created_object)

        return created_object

    def update(self, object_id: str, **kwargs) -> BaseModel | None:
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

    def increment(self, object_id: str, column: str):
        with Session(self.engine) as session:
            (
                session.
                query(self._model).
                filter_by(id=object_id).
                update({column: getattr(self._model, column) + 1})
            )
            session.commit()

    def decrement(self, object_id: str, column: str):
        with Session(self.engine) as session:
            (
                session.
                query(self._model).
                filter_by(id=object_id).
                update({column: getattr(self._model, column) - 1})
            )
            session.commit()
