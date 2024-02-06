from fastapi import Depends

from src.core.cache import Cache
from src.core.service import BaseService
from src.dish.model import DishModel
from src.menu.model import MenuModel
from src.menu.repository import Repository
from src.menu.schemas import CreateMenuSchema, MenuSchema, UpdateMenuSchema
from src.submenu.model import SubmenuModel
from src.submenu.repository import Repository as SubmenuRepository


class Service(BaseService):

    def __init__(
            self,
            repository=Depends(Repository),
            cache=Depends(Cache),
            submenu_repository=Depends(SubmenuRepository),
    ):
        self.repository = repository
        self.cache = cache
        self.submenu_repository = submenu_repository

    def get_all_menus(self) -> list[MenuModel]:
        return self.repository.get_all()

    def get_menu(self, menu_id: str) -> MenuModel | dict[str, str] | None:
        """
        Сервис для получения определённого меню.
        Проверяет наличие в кэше, если нет то достаёт из базы данных,
        кладёт в кэ и возвращает.
        """
        menu_from_caching: dict[str, str] = self.cache.get_value(menu_id)
        if menu_from_caching is not None:
            return menu_from_caching

        menu: MenuModel = self.repository.get(id=menu_id)
        if menu is None:
            return None

        self.cache.set_value(menu.id, menu, MenuSchema)

        return menu

    def create_menu(self, created_menu: CreateMenuSchema) -> MenuModel:
        """
        Сервис для создания нового меню.
        Созданное блюдо кладёт в кэш.
        """
        menu: MenuModel = self.repository.create(**created_menu.model_dump())
        self.cache.set_value(menu.id, menu, MenuSchema)

        return menu

    def update_menu(
            self,
            menu_id: str,
            updated_data: UpdateMenuSchema
    ) -> MenuModel | None:
        """
        Сервис для обновления меню.
        Данные о меню также обновляются в кэшэ.
        """
        updated_data_dict: dict[str, str] = self.delete_non_value_key(
            updated_data.model_dump()
        )

        self.cache.delete_value(menu_id)

        menu: MenuModel | None = self.repository.update(
            menu_id,
            **updated_data_dict
        )
        if menu is not None:
            self.cache.set_value(menu.id, menu, MenuSchema)

        return menu

    def delete_menu(self, menu_id: str):
        """Сервис для удаления меню."""
        self.cache.delete_value(menu_id)
        all_submenus: list[SubmenuModel] = self.submenu_repository.get_all(
            menu_id=menu_id
        )
        for submenu in all_submenus:
            self.cache.delete_value(submenu.id)

        all_dishes: list[DishModel] = self.repository.get_all_dishes(menu_id)
        for dish in all_dishes:
            self.cache.delete_value(dish.id)

        self.repository.delete(menu_id)
