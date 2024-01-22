from sqlalchemy.orm import Session

from src.core.repository import BaseRepository
from .model import MenuModel


class Repository(BaseRepository):
    _model = MenuModel

    def increment_submenu(self, menu_id: str):
        self.increment(menu_id, "submenus_count")

    def decrement_submenu(self, menu_id: str):
        self.decrement(menu_id, "submenus_count")

    def increment_dish(self, menu_id: str):
        self.increment(menu_id, "dishes_count")

    def decrement_dish(self, menu_id: str):
        self.decrement(menu_id, "dishes_count")

    def subtract_the_number_of_dishes(self, menu_id: str, count: int):
        with Session(self.engine) as session:
            (
                session.
                query(self._model).
                filter_by(id=menu_id).
                update({"dishes_count": self._model.dishes_count - count})
            )
            session.commit()
