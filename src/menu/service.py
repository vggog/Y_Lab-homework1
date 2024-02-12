from fastapi import BackgroundTasks, Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.core.cache import Cache
from src.core.service import BaseService
from src.menu.background_tasks import (
    create_menu_invalidate_cache,
    delete_menu_invalidate_cache,
    get_all_menus_invalidate_cache,
    get_invalidate_cache,
    set_full_base_cache,
    update_menu_invalidate_cache,
)
from src.menu.model import MenuModel
from src.menu.repository import Repository
from src.menu.schemas import CreateMenuSchema, MenuSchema, UpdateMenuSchema
from src.submenu.repository import Repository as SubmenuRepository


class Service(BaseService):

    def __init__(
            self,
            repository=Depends(Repository),
            cache=Depends(Cache),
            submenu_repository=Depends(SubmenuRepository),
    ):
        self.repository = repository
        self.cache = cache
        self.submenu_repository = submenu_repository

    async def full_base(
            self,
            background_tasks: BackgroundTasks,
            async_session: async_sessionmaker[AsyncSession]
    ) -> list[MenuModel] | list[dict[str, str]]:
        """Сервис для получения всех меню, со связанными подменю, со связанными блюдами."""
        key: str = self.get_key_for_all_datas('full_base')
        full_base_from_cache: list[dict[str, str]] = await self.cache.get_value(
            key
        )

        if full_base_from_cache is not None:
            return full_base_from_cache

        full_base: list[MenuModel] = await self.repository.get_full_base(
            async_session
        )

        background_tasks.add_task(
            set_full_base_cache,
            key=key,
            datas=full_base,
            cache=self.cache,
        )

        return full_base

    async def get_all_menus(
            self,
            background_tasks: BackgroundTasks,
            async_session: async_sessionmaker[AsyncSession]
    ) -> list[MenuModel] | list[dict[str, str]]:
        """Сервис для получения всех меню"""
        key: str = self.get_key_for_all_datas('menus')
        all_menus_from_cache: list[dict[str, str]] = await self.cache.get_value(
            key
        )

        if all_menus_from_cache is not None:
            return all_menus_from_cache

        all_menus: list[MenuModel] = await self.repository.get_all(
            async_session=async_session,
        )

        background_tasks.add_task(
            get_all_menus_invalidate_cache,
            key=key,
            datas=all_menus,
            cache=self.cache,
        )

        return all_menus

    async def get_menu(
            self,
            menu_id: str,
            background_tasks: BackgroundTasks,
            async_session: async_sessionmaker[AsyncSession],
    ) -> MenuModel | dict[str, str] | None:
        """
        Сервис для получения определённого меню.
        Проверяет наличие в кэше, если нет то достаёт из базы данных,
        кладёт в кэ и возвращает.
        """
        menu_from_caching: dict[str, str] = await self.cache.get_value(menu_id)
        if menu_from_caching is not None:
            return menu_from_caching

        menu: MenuModel = await self.repository.get(
            id=menu_id,
            async_session=async_session,
        )
        if menu is None:
            return None

        background_tasks.add_task(
            get_invalidate_cache,
            menu=menu,
            cache=self.cache,
        )

        await self.cache.set_value(menu.id, menu, MenuSchema)

        return menu

    async def create_menu(
            self,
            created_menu: CreateMenuSchema,
            background_tasks: BackgroundTasks,
            async_session: async_sessionmaker[AsyncSession],
    ) -> MenuModel:
        """
        Сервис для создания нового меню.
        Созданное блюдо кладёт в кэш.
        """
        menu: MenuModel = await self.repository.create(
            async_session=async_session,
            **created_menu.model_dump(),
        )
        background_tasks.add_task(
            create_menu_invalidate_cache,
            menu_id=menu.id,
            menu=menu,
            cache=self.cache,
        )
        return menu

    async def update_menu(
            self,
            menu_id: str,
            updated_data: UpdateMenuSchema,
            background_tasks: BackgroundTasks,
            async_session: async_sessionmaker[AsyncSession],
    ) -> MenuModel | None:
        """
        Сервис для обновления меню.
        Данные о меню также обновляются в кэшэ.
        """
        updated_data_dict: dict[str, str] = self.delete_non_value_key(
            updated_data.model_dump()
        )

        menu: MenuModel | None = await self.repository.update(
            menu_id,
            async_session=async_session,
            **updated_data_dict,
        )
        if menu is None:
            return None

        background_tasks.add_task(
            update_menu_invalidate_cache,
            menu_id=menu_id,
            menu=menu,
            cache=self.cache,
        )

        return menu

    async def delete_menu(
            self,
            menu_id: str,
            background_tasks: BackgroundTasks,
            async_session: async_sessionmaker[AsyncSession]
    ) -> None:
        """Сервис для удаления меню."""

        background_tasks.add_task(
            delete_menu_invalidate_cache,
            menu_id=menu_id,
            async_session=async_session,
            cache=self.cache,
            menu_repository=self.repository,
            submenu_repository=self.submenu_repository,
        )

        await self.repository.delete(
            menu_id,
            async_session=async_session,
        )
