from fastapi import Depends

from src.core.cache import Cache
from src.core.service import BaseService
from src.submenu.model import SubmenuModel
from src.submenu.repository import Repository
from src.submenu.schemas import CreateSubmenuSchema, SubmenuSchema, UpdateSubmenuSchema


class Service(BaseService):

    def __init__(
            self,
            repository=Depends(Repository),
            cache=Depends(Cache),
    ):
        self.repository = repository
        self.cache = cache

    def get_all_submenu(
            self,
            menu_id: str
    ) -> list[SubmenuModel] | list[dict[str, str]]:
        key = self.get_key_for_all_datas('submenus', menu_id)
        all_submenus_from_cache = self.cache.get_value(key)
        if all_submenus_from_cache is not None:
            return all_submenus_from_cache

        all_submenus: list[SubmenuModel] = self.repository.get_all(
            menu_id=menu_id
        )

        self.cache.set_list_of_values(
            key=key,
            datas=all_submenus,
            schema=SubmenuSchema,
        )

        return all_submenus

    def get_submenu(
            self,
            submenu_id: str
    ) -> SubmenuModel | dict[str, str] | None:
        """Сервис для получения подменю."""
        submenu_from_cache: dict[str, str] = self.cache.get_value(submenu_id)
        if submenu_from_cache is not None:
            return submenu_from_cache

        submenu: SubmenuModel = self.repository.get(id=submenu_id)
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
        """
        Метод для создания меню.
        Созданное меню добавляется в кэш.
        """
        submenu: SubmenuModel = self.repository.create(
            menu_id=menu_id,
            **created_submenu.model_dump(),
        )
        self.cache.set_value(
            key=submenu.id,
            data=submenu,
            schema=SubmenuSchema,
        )
        self.cache.delete_value(menu_id)
        self.cache.delete_value(
            key=self.get_key_for_all_datas('submenus', menu_id)
        )
        self.cache.delete_value(
            key=self.get_key_for_all_datas('menus')
        )

        return submenu

    def update_submenu(
            self,
            submenu_id: str,
            updated_data: UpdateSubmenuSchema,
    ) -> SubmenuModel | None:
        """
        Сервис для обновления подменю.
        Данные о подменю обновляются в кэше.
        """
        updated_data_dict: dict[str, str] = self.delete_non_value_key(
            updated_data.model_dump()
        )

        self.cache.delete_value(submenu_id)

        submenu: SubmenuModel | None = self.repository.update(
            submenu_id,
            **updated_data_dict
        )

        if submenu is not None:
            self.cache.set_value(
                key=submenu.id,
                data=submenu,
                schema=SubmenuSchema,
            )
        return submenu

    def delete_submenu(self, menu_id: str, submenu_id: str):
        """Сервис для удаления подменю."""
        self.cache.delete_value(menu_id)
        self.cache.delete_value(submenu_id)
        self.cache.delete_value(
            key=self.get_key_for_all_datas('submenus', menu_id)
        )
        self.cache.delete_value(
            key=self.get_key_for_all_datas('menus')
        )

        self.repository.delete(submenu_id)
