from fastapi import Depends

from src.core.cache import Cache
from src.core.service import BaseService
from src.submenu.repository import Repository as SubmenuRepository

from .model import MenuModel
from .repository import Repository
from .schemas import CreateMenuSchema, MenuSchema, UpdateMenuSchema


class Service(BaseService):

    def __init__(
            self,
            repository=Depends(Repository),
            cache=Depends(Cache),
            submenu_repository=Depends(SubmenuRepository)
    ):
        self.repository = repository
        self.cache = cache
        self.submenu_repository = submenu_repository

    def get_all_menus(self) -> list[MenuModel]:
        return self.repository.get_all()

    def get_menu(self, menu_id: str) -> MenuModel | None:
        menu_from_caching = self.cache.get_value(menu_id)
        if menu_from_caching is not None:
            return menu_from_caching

        menu: MenuModel = self.repository.get_by_id(menu_id)
        if menu is None:
            return None

        self.cache.set_value(menu.id, menu, MenuSchema)

        return menu

    def create_menu(self, created_menu: CreateMenuSchema):
        menu: MenuModel = self.repository.create(**created_menu.model_dump())
        self.cache.set_value(menu.id, menu, MenuSchema)

        return menu

    def update_menu(
            self,
            menu_id: str,
            updated_data: UpdateMenuSchema
    ) -> MenuModel:
        updated_data_dict = {
            k: v for k, v in updated_data.model_dump().items() if v is not None
        }

        self.cache.delete_value(menu_id)

        menu = self.repository.update(menu_id, **updated_data_dict)
        self.cache.set_value(menu.id, menu, MenuSchema)

        return menu

    def delete_menu(self, menu_id: str):
        self.cache.delete_value(menu_id)
        all_submenus = self.submenu_repository.get_all_submenus_of_menu(
            menu_id
        )
        for submenu in all_submenus:
            self.cache.delete_value(submenu.id)

        all_dishes = self.repository.get_all_dishes(menu_id)
        for dish in all_dishes:
            print(dish)
            self.cache.delete_value(dish.id)

        return self.repository.delete(menu_id)
