from fastapi import BackgroundTasks, Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.core.cache import Cache
from src.core.db_session import get_db_session
from src.core.service import BaseService
from src.submenu.background_tasks import (
    create_invalidate_cache,
    delete_submenu_invalidate_cache,
    get_all_submenus_invalidate_cache,
    get_invalidate_cache,
    update_submenu_invalidate_cache,
)
from src.submenu.model import SubmenuModel
from src.submenu.repository import Repository
from src.submenu.schemas import CreateSubmenuSchema, UpdateSubmenuSchema


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

    async def get_all_submenu(
            self,
            menu_id: str,
            background_tasks: BackgroundTasks,
    ) -> list[SubmenuModel] | list[dict[str, str]]:
        key = self.get_key_for_all_datas('submenus', menu_id)
        all_submenus_from_cache = await self.cache.get_value(key)
        if all_submenus_from_cache is not None:
            return all_submenus_from_cache

        all_submenus: list[SubmenuModel] = await self.repository.get_all(
            menu_id=menu_id,
            async_session=self.async_session,
        )

        background_tasks.add_task(
            get_all_submenus_invalidate_cache,
            key=key,
            datas=all_submenus,
            cache=self.cache,
        )

        return all_submenus

    async def get_submenu(
            self,
            submenu_id: str,
            background_tasks: BackgroundTasks,
    ) -> SubmenuModel | dict[str, str] | None:
        """Сервис для получения подменю."""
        submenu_from_cache: dict[str, str] = await self.cache.get_value(
            submenu_id
        )
        if submenu_from_cache is not None:
            return submenu_from_cache

        submenu: SubmenuModel = await self.repository.get(
            id=submenu_id,
            async_session=self.async_session,
        )
        if submenu is None:
            return None

        background_tasks.add_task(
            get_invalidate_cache,
            submenu=submenu,
            cache=self.cache,
        )

        return submenu

    async def create_submenu(
            self,
            menu_id: str,
            background_tasks: BackgroundTasks,
            created_submenu: CreateSubmenuSchema,
    ) -> SubmenuModel:
        """
        Метод для создания меню.
        Созданное меню добавляется в кэш.
        """
        submenu: SubmenuModel = await self.repository.create(
            menu_id=menu_id,
            async_session=self.async_session,
            **created_submenu.model_dump(),
        )

        background_tasks.add_task(
            create_invalidate_cache,
            menu_id=menu_id,
            submenu=submenu,
            cache=self.cache,
        )

        return submenu

    async def update_submenu(
            self,
            submenu_id: str,
            background_tasks: BackgroundTasks,
            updated_data: UpdateSubmenuSchema,
    ) -> SubmenuModel | None:
        """
        Сервис для обновления подменю.
        Данные о подменю обновляются в кэше.
        """
        updated_data_dict: dict[str, str] = self.delete_non_value_key(
            updated_data.model_dump()
        )

        await self.cache.delete_value(submenu_id)

        submenu: SubmenuModel | None = await self.repository.update(
            submenu_id,
            async_session=self.async_session,
            **updated_data_dict
        )

        if submenu is None:
            return None

        background_tasks.add_task(
            update_submenu_invalidate_cache,
            submenu_id=submenu_id,
            submenu=submenu,
            cache=self.cache,
        )

        return submenu

    async def delete_submenu(
            self,
            menu_id: str,
            submenu_id: str,
            background_tasks: BackgroundTasks,
    ):
        """Сервис для удаления подменю."""
        background_tasks.add_task(
            delete_submenu_invalidate_cache,
            menu_id=menu_id,
            submenu_id=submenu_id,
            cache=self.cache,
        )

        await self.repository.delete(
            submenu_id,
            async_session=self.async_session,
        )
