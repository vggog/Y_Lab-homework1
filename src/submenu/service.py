from fastapi import Depends

from .repository import Repository
from src.menu.repository import Repository as MenuRepository
from .schemas import CreateSubmenuSchema, UpdateSubmenuSchema, SubmenuSchema
from .model import SubmenuModel
from src.core.cache import Cache


class Service:

    def __init__(
            self,
            repository=Depends(Repository),
            menu_repository=Depends(MenuRepository),
            cache=Depends(Cache),
    ):
        self.repository = repository
        self.menu_repository = menu_repository
        self.cache = cache

    def get_all_submenu(self, menu_id: str):
        return self.repository.get_all_submenus_of_menu(menu_id)

    def get_submenu(self, submenu_id: str, menu_id: str):
        submenu_from_cache = self.cache.get_value(submenu_id)
        if submenu_from_cache is not None:
            return submenu_from_cache

        submenu = self.repository.get_submenu(
            submenu_id=submenu_id, menu_id=menu_id
        )
        if submenu is None:
            return None

        self.cache.set_value(
            key=submenu.id,
            data=submenu,
            schema=SubmenuSchema,
        )

        return submenu

    def create_submenu(
            self,
            menu_id: str,
            created_submenu: CreateSubmenuSchema
    ) -> SubmenuModel:
        submenu = self.repository.create(
            menu_id=menu_id,
            **created_submenu.model_dump(),
        )
        self.cache.set_value(
            key=submenu.id,
            data=submenu,
            schema=SubmenuSchema,
        )
        self.cache.delete_value(menu_id)

        return submenu

    def update_submenu(
            self,
            submenu_id: str,
            updated_data: UpdateSubmenuSchema,
    ) -> SubmenuModel:
        updated_data_dict = {
            k: v for k, v in updated_data.model_dump().items() if v is not None
        }

        self.cache.delete_value(submenu_id)

        submenu = self.repository.update(submenu_id, **updated_data_dict)

        self.cache.set_value(
            key=submenu.id,
            data=submenu,
            schema=SubmenuSchema,
        )
        return submenu

    def delete_submenu(self, menu_id: str, submenu_id: str):
        self.cache.delete_value(menu_id)
        self.cache.delete_value(submenu_id)
        self.repository.delete(submenu_id)
