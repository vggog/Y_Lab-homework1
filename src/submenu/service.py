from fastapi import Depends

from .repository import Repository
from .schemas import CreateSubmenuSchema, UpdateSubmenuSchema
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
