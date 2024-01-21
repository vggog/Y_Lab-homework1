from fastapi import Depends

from .repository import Repository
from .schemas import CreateSubmenuSchema
from .model import SubmenuModel


class Service:

    def __init__(
            self,
            repository=Depends(Repository),
    ):
        self.repository = repository

    def get_all_submenu(self, menu_id: str):
        return self.repository.get_all_submenus_of_menu(menu_id)

    def get_submenu(self, submenu_id: str, menu_id: str):
        return self.repository.get_submenu(
            submenu_id=submenu_id, menu_id=menu_id
        )

    def create_submenu(
            self,
            menu_id: str,
            created_submenu: CreateSubmenuSchema
    ) -> SubmenuModel:
        return self.repository.create(
            menu_id=menu_id, **created_submenu.model_dump()
        )
