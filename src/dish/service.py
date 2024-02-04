from fastapi import Depends

from src.core.cache import Cache
from src.menu.repository import Repository as MenuRepository
from src.submenu.repository import Repository as SubmenuRepository

from .model import DishModel
from .repository import Repository
from .schemas import CreateDishSchema, DishSchema, UpdateDishSchema


class Service:

    def __init__(
            self,
            repository=Depends(Repository),
            menu_repository=Depends(MenuRepository),
            submenu_repository=Depends(SubmenuRepository),
            cache=Depends(Cache)
    ):
        self.repository = repository
        self.menu_repository = menu_repository
        self.submenu_repository = submenu_repository
        self.cache = cache

    def get_all_dishes(self):
        return self.repository.get_all()

    def get_dish(self, dish_id: str) -> DishModel | None:
        dish_from_cache = self.cache.get_value(dish_id)
        if dish_from_cache is not None:
            return dish_from_cache

        dish = self.repository.get_by_id(dish_id)
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
        dish = self.repository.create(
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

        return dish

    def update_dish(
            self,
            dish_id: str,
            updated_data: UpdateDishSchema
    ) -> DishModel:
        updated_data_dict = {
            k: v for k, v in updated_data.model_dump().items() if v is not None
        }

        self.cache.delete_value(dish_id)
        dish = self.repository.update(dish_id, **updated_data_dict)
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
        self.cache.delete_value(menu_id)
        self.cache.delete_value(submenu_id)
        self.cache.delete_value(dish_id)

        self.repository.delete(dish_id)
