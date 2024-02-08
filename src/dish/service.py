from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.core.cache import Cache
from src.core.db_session import get_db_session
from src.core.service import BaseService
from src.dish.model import DishModel
from src.dish.repository import Repository
from src.dish.schemas import CreateDishSchema, DishSchema, UpdateDishSchema


class Service(BaseService):

    def __init__(
            self,
            repository=Depends(Repository),
            cache=Depends(Cache),
            async_session: async_sessionmaker[AsyncSession] = Depends(
                get_db_session
            ),
    ):
        self.async_session = async_session
        self.repository = repository
        self.cache = cache

    async def get_all_dishes(
            self,
            submenu_id: str
    ) -> list[DishSchema] | dict[str, str]:
        key: str = self.get_key_for_all_datas('dishes', submenu_id)
        all_dishes_from_cache: dict[str, str] | None = await self.cache.get_value(
            key=key
        )
        if all_dishes_from_cache is not None:
            return all_dishes_from_cache

        all_dishes = await self.repository.get_all(
            submenu_id=submenu_id,
            async_session=self.async_session,
        )

        await self.cache.set_list_of_values(
            key=key,
            datas=all_dishes,
            schema=DishSchema,
        )

        return all_dishes

    async def get_dish(self, dish_id: str) -> DishModel | dict[str, str] | None:
        """
        Сервис для получения определённого блюда.
        Проверяет наличие в кэше, если нет то достаёт из базы данных,
        кладёт в кэш и возвращает.
        """
        dish_from_cache: dict[str, str] = await self.cache.get_value(dish_id)
        if dish_from_cache is not None:
            return dish_from_cache

        dish: DishModel | None = await self.repository.get(
            id=dish_id,
            async_session=self.async_session,
        )
        if dish is None:
            return None

        await self.cache.set_value(
            key=dish.id,
            data=dish,
            schema=DishSchema,
        )

        return dish

    async def create_dish(
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
        dish: DishModel = await self.repository.create(
            submenu_id=submenu_id,
            async_session=self.async_session,
            **created_dish.model_dump()
        )

        await self.cache.set_value(
            key=dish.id,
            data=dish,
            schema=DishSchema,
        )

        await self.cache.delete_value(menu_id)
        await self.cache.delete_value(submenu_id)
        await self.cache.delete_value(
            key=self.get_key_for_all_datas('dishes', submenu_id)
        )
        await self.cache.delete_value(
            key=self.get_key_for_all_datas('submenus', menu_id)
        )
        await self.cache.delete_value(
            key=self.get_key_for_all_datas('menus')
        )

        return dish

    async def update_dish(
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

        await self.cache.delete_value(dish_id)
        dish: DishModel | None = await self.repository.update(
            dish_id,
            async_session=self.async_session,
            **updated_data_dict,
        )
        await self.cache.set_value(
            key=dish_id,
            data=dish,
            schema=DishSchema,
        )

        return dish

    async def delete_dish(
            self,
            menu_id: str,
            submenu_id: str,
            dish_id: str
    ):
        """
        Сервис для удаления блюда.
        Для инвалидации удаляет связанные с блюдом меню и подменю.
        """
        await self.cache.delete_value(menu_id)
        await self.cache.delete_value(submenu_id)
        await self.cache.delete_value(dish_id)
        await self.cache.delete_value(
            key=self.get_key_for_all_datas('dishes', submenu_id)
        )
        await self.cache.delete_value(
            key=self.get_key_for_all_datas('submenus', menu_id)
        )
        await self.cache.delete_value(
            key=self.get_key_for_all_datas('menus')
        )

        await self.repository.delete(
            dish_id,
            async_session=self.async_session,
        )
