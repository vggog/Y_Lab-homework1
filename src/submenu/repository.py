from src.core.repository import BaseRepository
from src.submenu.model import SubmenuModel


class Repository(BaseRepository):
    _model = SubmenuModel

    def get_all_submenus_of_menu(self, menu_id) -> list:
        return self.get_all(menu_id=menu_id)

    def get_submenu(self, menu_id: str, submenu_id: str):
        return self.get(id=submenu_id, menu_id=menu_id)
