from fastapi import Depends

from .repository import Repository
from src.menu.repository import Repository as MenuRepository
from src.submenu.repository import Repository as SubmenuRepository
from .schemas import CreateDishSchema, UpdateDishSchema
from .model import DishModel


class Service:

    def __init__(
            self,
            repository=Depends(Repository),
            menu_repository=Depends(MenuRepository),
            submenu_repository=Depends(SubmenuRepository),
    ):
        self.repository = repository
        self.menu_repository = menu_repository
        self.submenu_repository = submenu_repository

    def get_all_dishes(self):
        return self.repository.get_all()

    def get_dish(self, dish_id: str) -> DishModel:
        return self.repository.get_by_id(dish_id)

    def create_dish(
            self,
            menu_id: int,
            submenu_id: str,
            created_dish: CreateDishSchema
    ) -> DishModel:
        dish = self.repository.create(
            submenu_id=submenu_id,
            **created_dish.model_dump()
        )

        self.submenu_repository.increment_dish(submenu_id)
        self.menu_repository.increment_dish(menu_id)

        return dish

    def update_dish(
            self,
            dish_id: str,
            updated_data: UpdateDishSchema
    ) -> DishModel:
        updated_data_dict = {
            k: v for k, v in updated_data.model_dump().items() if v is not None
        }

        return self.repository.update(dish_id, **updated_data_dict)

    def delete_dish(
            self,
            menu_id: int,
            submenu_id: str,
            dish_id: str
    ):
        if self.repository.get_by_id(dish_id):
            self.submenu_repository.decrement_dish(submenu_id)
            self.menu_repository.decrement_dish(menu_id)

        self.repository.delete(dish_id)
