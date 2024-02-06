from fastapi import Depends

from src.core.cache import Cache
from src.core.service import BaseService
from src.dish.model import DishModel
from src.dish.repository import Repository
from src.dish.schemas import CreateDishSchema, DishSchema, UpdateDishSchema


class Service(BaseService):

    def __init__(
            self,
            repository=Depends(Repository),
            cache=Depends(Cache),
    ):
        self.repository = repository
        self.cache = cache

    def get_all_dishes(
            self,
            submenu_id: str
    ) -> list[DishSchema] | dict[str, str]:
        key: str = self.get_key_for_all_datas('dishes', submenu_id)
        all_dishes_from_cache: dict[str, str] | None = self.cache.get_value(
            key=key
        )
        if all_dishes_from_cache is not None:
            return all_dishes_from_cache

        all_dishes = self.repository.get_all(submenu_id=submenu_id)

        self.cache.set_list_of_values(
            key=key,
            datas=all_dishes,
            schema=DishSchema,
        )

        return all_dishes

    def get_dish(self, dish_id: str) -> DishModel | dict[str, str] | None:
        """
        Сервис для получения определённого блюда.
        Проверяет наличие в кэше, если нет то достаёт из базы данных,
        кладёт в кэш и возвращает.
        """
        dish_from_cache: dict[str, str] = self.cache.get_value(dish_id)
        if dish_from_cache is not None:
            return dish_from_cache

        dish: DishModel | None = self.repository.get(id=dish_id)
        if dish is None:
            return None

        self.cache.set_value(
            key=dish.id,
            data=dish,
            schema=DishSchema,
        )

        return dish

    def create_dish(
            self,
            menu_id: str,
            submenu_id: str,
            created_dish: CreateDishSchema
    ) -> DishModel:
        """
        Сорвис для создания нового блюда.
        Созданное блюдо кладёт в кэш.
        Для инвалидации удаляет связанные с блюдом меню и подменю.
        """
        dish: DishModel = self.repository.create(
            submenu_id=submenu_id,
            **created_dish.model_dump()
        )

        self.cache.set_value(
            key=dish.id,
            data=dish,
            schema=DishSchema,
        )

        self.cache.delete_value(menu_id)
        self.cache.delete_value(submenu_id)
        self.cache.delete_value(
            key=self.get_key_for_all_datas('dishes', submenu_id)
        )
        self.cache.delete_value(
            key=self.get_key_for_all_datas('submenus', menu_id)
        )
        self.cache.delete_value(
            key=self.get_key_for_all_datas('menus')
        )

        return dish

    def update_dish(
            self,
            dish_id: str,
            updated_data: UpdateDishSchema
    ) -> DishModel | None:
        """
        Сервис для обновления блюда.
        Данные о блюде также обновляются в кэшэ.
        """
        updated_data_dict: dict[str, str] = self.delete_non_value_key(
            updated_data.model_dump()
        )

        self.cache.delete_value(dish_id)
        dish: DishModel | None = self.repository.update(
            dish_id,
            **updated_data_dict
        )
        self.cache.set_value(
            key=dish_id,
            data=dish,
            schema=DishSchema,
        )

        return dish

    def delete_dish(
            self,
            menu_id: str,
            submenu_id: str,
            dish_id: str
    ):
        """
        Сервис для удаления блюда.
        Для инвалидации удаляет связанные с блюдом меню и подменю.
        """
        self.cache.delete_value(menu_id)
        self.cache.delete_value(submenu_id)
        self.cache.delete_value(dish_id)
        self.cache.delete_value(
            key=self.get_key_for_all_datas('dishes', submenu_id)
        )
        self.cache.delete_value(
            key=self.get_key_for_all_datas('submenus', menu_id)
        )
        self.cache.delete_value(
            key=self.get_key_for_all_datas('menus')
        )

        self.repository.delete(dish_id)
