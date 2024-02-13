from fastapi import BackgroundTasks, Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.core.cache import Cache
from src.core.db_session import get_db_session
from src.core.service import BaseService
from src.dish.background_tasks import (
    create_dish_invalidate_cache,
    delete_dish_invalidate_cache,
    set_all_dishes_invalidate_cache,
    set_dish_invalidate_cache,
    update_dish_invalidate_cache,
)
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

    async def _price_with_discount(self, price: float, dish_id: str) -> float:
        """Выдаёт цену за блюдо с учётом скидки."""
        discount: int = await self.cache.get_discount_of_dish(dish_id)

        return price * ((100 - discount) / 100)

    async def get_all_dishes(
            self,
            submenu_id: str,
            background_tasks: BackgroundTasks,
    ) -> list[DishSchema] | dict[str, str]:
        """Сервис для получения всех блюд"""
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

        for dish in all_dishes:
            dish.price = str(
                await self._price_with_discount(float(dish.price), dish.id)
            )

        background_tasks.add_task(
            set_all_dishes_invalidate_cache,
            key=key,
            datas=all_dishes,
            cache=self.cache,
        )

        return all_dishes

    async def get_dish(
            self,
            dish_id: str,
            background_tasks: BackgroundTasks,
    ) -> DishModel | dict[str, str] | None:
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

        dish.price = str(
            await self._price_with_discount(float(dish.price), dish.id)
        )

        background_tasks.add_task(
            set_dish_invalidate_cache,
            dish=dish,
            cache=self.cache,
        )

        return dish

    async def create_dish(
            self,
            menu_id: str,
            submenu_id: str,
            created_dish: CreateDishSchema,
            background_tasks: BackgroundTasks,
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

        background_tasks.add_task(
            create_dish_invalidate_cache,
            menu_id=menu_id,
            submenu_id=submenu_id,
            dish=dish,
            cache=self.cache,
        )

        return dish

    async def update_dish(
            self,
            dish_id: str,
            updated_data: UpdateDishSchema,
            background_tasks: BackgroundTasks,
    ) -> DishModel | None:
        """
        Сервис для обновления блюда.
        Данные о блюде также обновляются в кэшэ.
        """
        updated_data_dict: dict[str, str] = self.delete_non_value_key(
            updated_data.model_dump()
        )

        dish: DishModel | None = await self.repository.update(
            dish_id,
            async_session=self.async_session,
            **updated_data_dict,
        )
        if dish is None:
            return dish

        dish.price = str(
            await self._price_with_discount(float(dish.price), dish.id)
        )

        background_tasks.add_task(
            update_dish_invalidate_cache,
            dish_id=dish_id,
            dish=dish,
            cache=self.cache,
        )

        return dish

    async def delete_dish(
            self,
            menu_id: str,
            submenu_id: str,
            dish_id: str,
            background_tasks: BackgroundTasks,
    ) -> None:
        """
        Сервис для удаления блюда.
        Для инвалидации удаляет связанные с блюдом меню и подменю.
        """
        background_tasks.add_task(
            delete_dish_invalidate_cache,
            dish_id=dish_id,
            submenu_id=submenu_id,
            menu_id=menu_id,
            cache=self.cache,
        )

        await self.repository.delete(
            dish_id,
            async_session=self.async_session,
        )
