from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.core.cache import Cache
from src.core.db_session import get_db_session
from src.core.service import BaseService
from src.menu.model import MenuModel
from src.menu.repository import Repository as MenuRepository
from src.menu.schemas import MenuFullBaseSchema, MenuSchema
from src.submenu.repository import Repository as SubmenuRepository


async def set_full_base_cache(
        key: str,
        datas: list,
        cache: Cache,
):
    """Добавление всей базы данных в кэш"""
    await cache.set_list_of_values(
        key=key,
        datas=datas,
        schema=MenuFullBaseSchema,
    )


async def create_menu_invalidate_cache(
        menu_id: str,
        menu: MenuModel,
        cache: Cache,
):
    """Ивалидация кэша при создание меню"""
    await cache.set_value(menu_id, menu, MenuSchema)
    await cache.delete_value(BaseService.get_key_for_all_datas('menus'))
    await cache.delete_value(BaseService.get_key_for_all_datas('full_base'))


async def update_menu_invalidate_cache(
        menu_id: str,
        menu: MenuModel,
        cache: Cache,
):
    """Инвалидация кэша при обновление меню"""
    await cache.delete_value(menu_id)
    await cache.set_value(menu_id, menu, MenuSchema)


async def get_all_menus_invalidate_cache(
        key: str,
        datas: list,
        cache: Cache,
):
    """Добавление всех меню в кэш"""
    await cache.set_list_of_values(
        key=key,
        datas=datas,
        schema=MenuSchema,
    )


async def get_invalidate_cache(
        menu: MenuModel,
        cache: Cache,
):
    """Добавление меню в кэш"""
    await cache.set_value(menu.id, menu, MenuSchema)


async def delete_menu_invalidate_cache(
        menu_id: str,
        cache: Cache,
        submenu_repository: SubmenuRepository,
        menu_repository: MenuRepository,
        async_session: async_sessionmaker[AsyncSession] = Depends(
            get_db_session
        ),
):
    """Инвалидация кэша при удаление меню."""
    await cache.delete_value(menu_id)

    all_submenus = await submenu_repository.get_all(
        menu_id=menu_id,
        async_session=async_session,
    )

    for submenu in all_submenus:
        await cache.delete_value(submenu.id)

    all_dishes = await menu_repository.get_all_dishes(
        menu_id,
        async_session=async_session,
    )
    for dish in all_dishes:
        await cache.delete_value(dish.id)

    await cache.delete_value(BaseService.get_key_for_all_datas('menus'))
    await cache.delete_value(BaseService.get_key_for_all_datas('full_base'))
