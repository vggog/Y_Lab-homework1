from fastapi import Depends

from src.menu.repository import Repository as MenuRepository

from .model import SubmenuModel
from .repository import Repository
from .schemas import CreateSubmenuSchema, UpdateSubmenuSchema


class Service:

    def __init__(
            self,
            repository=Depends(Repository),
            menu_repository=Depends(MenuRepository),
    ):
        self.repository = repository
        self.menu_repository = menu_repository

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
        submenu = self.repository.create(
            menu_id=menu_id,
            **created_submenu.model_dump(),
        )

        return submenu

    def update_submenu(
            self,
            submenu_id: str,
            updated_data: UpdateSubmenuSchema,
    ) -> SubmenuModel:
        updated_data_dict = {
            k: v for k, v in updated_data.model_dump().items() if v is not None
        }

        return self.repository.update(submenu_id, **updated_data_dict)

    def delete_submenu(self, submenu_id: str):
        self.repository.delete(submenu_id)
