from fastapi import Depends

from src.core.service import BaseService
from .repository import Repository
from .model import MenuModel
from .schemas import CreateMenuSchema


class Service(BaseService):

    def __init__(
            self,
            repository=Depends(Repository)
    ):
        self.repository = repository

    def get_all_menus(self) -> list[MenuModel]:
        return self.repository.get_all()

    def create_menu(self, created_menu: CreateMenuSchema):
        return self.repository.create(**created_menu.model_dump())
