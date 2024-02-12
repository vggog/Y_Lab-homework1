from src.core.cache import Cache
from src.core.service import BaseService
from src.submenu.model import SubmenuModel
from src.submenu.schemas import SubmenuSchema


async def get_all_submenus_invalidate_cache(
        key: str,
        datas: list,
        cache: Cache,
):
    """Сохранение всех сабменю в кэш"""
    await cache.set_list_of_values(
        key=key,
        datas=datas,
        schema=SubmenuSchema,
    )


async def get_invalidate_cache(
        submenu: SubmenuModel,
        cache: Cache,
):
    """Сохраниение подменю в кэш"""
    await cache.set_value(submenu.id, submenu, SubmenuSchema)


async def create_invalidate_cache(
        menu_id: str,
        submenu: SubmenuModel,
        cache: Cache,
):
    """Инвалидация кэша при создание подменю"""
    await cache.set_value(
        key=submenu.id,
        data=submenu,
        schema=SubmenuSchema,
    )
    await cache.delete_value(menu_id)
    await cache.delete_value(
        key=BaseService.get_key_for_all_datas('submenus', menu_id)
    )
    await cache.delete_value(
        key=BaseService.get_key_for_all_datas('full_base')
    )


async def update_submenu_invalidate_cache(
        submenu_id: str,
        submenu: SubmenuModel,
        cache: Cache,
):
    """Инвалидация кэша при обновление подменю"""
    await cache.delete_value(submenu_id)
    await cache.set_value(submenu_id, submenu, SubmenuSchema)


async def delete_submenu_invalidate_cache(
        menu_id: str,
        submenu_id: str,
        cache: Cache,
):
    """Инвалидация кэша при удаление подменю"""
    await cache.delete_value(menu_id)
    await cache.delete_value(submenu_id)
    await cache.delete_value(
        key=BaseService.get_key_for_all_datas('submenus', menu_id)
    )
    await cache.delete_value(
        key=BaseService.get_key_for_all_datas('full_base')
    )
