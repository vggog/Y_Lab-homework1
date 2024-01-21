from sqlalchemy.orm import Session

from src.core.repository import BaseRepository
from .model import SubmenuModel


class Repository(BaseRepository):
    _model = SubmenuModel

    def get_all_submenus_of_menu(self, menu_id) -> list:
        return self.get_all_by_filter(menu_id=menu_id)
