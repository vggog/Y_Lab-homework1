from fastapi import Depends

from .repository import Repository
from .schemas import CreateDishSchema


class Service:

    def __init__(
            self,
            repository=Depends(Repository),
    ):
        self.repository = repository

    def get_all_dishes(self):
        return self.repository.get_all()

    def create_dish(self, submenu_id: str, created_dish: CreateDishSchema):
        return self.repository.create(
            submenu_id=submenu_id,
            **created_dish.model_dump()
        )
