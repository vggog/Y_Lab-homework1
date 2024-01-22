from sqlalchemy.orm import Session

from src.core.repository import BaseRepository
from .model import SubmenuModel


class Repository(BaseRepository):
    _model = SubmenuModel

    def get_all_submenus_of_menu(self, menu_id) -> list:
        return self.get_all_by_filter(menu_id=menu_id)

    def get_submenu(self, menu_id: str, submenu_id: str):
        return self.get(id=submenu_id, menu_id=menu_id)

    def increment_dish(self, submenu_id: str):
        self.increment(submenu_id, "dishes_count")

    def decrement_dish(self, submenu_id: str):
        self.decrement(submenu_id, "dishes_count")
