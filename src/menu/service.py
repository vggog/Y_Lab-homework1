from fastapi import Depends

from src.core.service import BaseService
from .repository import Repository
from .model import MenuModel
from .schemas import CreateMenuSchema, UpdateMenuSchema


class Service(BaseService):

    def __init__(
            self,
            repository=Depends(Repository)
    ):
        self.repository = repository

    def get_all_menus(self) -> list[MenuModel]:
        return self.repository.get_all()

    def get_menu(self, menu_id: int) -> MenuModel:
        return self.repository.get_by_id(menu_id)

    def create_menu(self, created_menu: CreateMenuSchema):
        return self.repository.create(**created_menu.model_dump())

    def update_menu(
            self,
            menu_id: int,
            updated_data: UpdateMenuSchema
    ) -> MenuModel:
        updated_data_dict = {
            k: v for k, v in updated_data.model_dump().items() if v is not None
        }

        return self.repository.update(menu_id, **updated_data_dict)

    def delete_menu(self, menu_id: int):
        return self.repository.delete(menu_id)
