from sqlalchemy.orm import Session

from src.core.repository import BaseRepository
from src.dish.model import DishModel


class Repository(BaseRepository):
    _model = DishModel

    def get_by_id(self, object_id: str) -> DishModel | None:
        with Session(self.engine) as session:
            return session.query(self._model).filter_by(id=object_id).first()
