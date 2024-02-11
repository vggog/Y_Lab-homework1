from src.core.cache import Cache
from src.core.service import BaseService
from src.dish.model import DishModel
from src.dish.schemas import DishSchema


async def set_all_dishes_invalidate_cache(
        key: str,
        datas: list,
        cache: Cache,
):
    """Сохранить все блюда в кэш"""
    await cache.set_list_of_values(
        key=key,
        datas=datas,
        schema=DishSchema,
    )


async def set_dish_invalidate_cache(
        dish: DishModel,
        cache: Cache,
):
    """Сохранить блюдо в кэш"""
    await cache.set_value(
        key=dish.id,
        data=dish,
        schema=DishSchema,
    )


async def create_dish_invalidate_cache(
        menu_id: str,
        submenu_id: str,
        dish: DishModel,
        cache: Cache,
):
    """Инвалидация кэша при создание блюда"""
    await cache.set_value(
        key=dish.id,
        data=dish,
        schema=DishSchema,
    )

    await cache.delete_value(menu_id)
    await cache.delete_value(submenu_id)
    await cache.delete_value(
        key=BaseService.get_key_for_all_datas('dishes', submenu_id)
    )
    await cache.delete_value(
        key=BaseService.get_key_for_all_datas('submenus', menu_id)
    )
    await cache.delete_value(
        key=BaseService.get_key_for_all_datas('menus')
    )


async def update_dish_invalidate_cache(
        dish_id: str,
        dish: DishModel,
        cache: Cache,
):
    """Инвалидация кэша при обновление блюда"""
    await cache.delete_value(dish_id)

    await cache.set_value(
        key=dish_id,
        data=dish,
        schema=DishSchema,
    )


async def delete_dish_invalidate_cache(
        menu_id: str,
        submenu_id: str,
        dish_id: str,
        cache: Cache,
):
    """Инвалидация кэша при удаление блюда"""
    await cache.delete_value(menu_id)
    await cache.delete_value(submenu_id)
    await cache.delete_value(dish_id)
    await cache.delete_value(
        key=BaseService.get_key_for_all_datas('dishes', submenu_id)
    )
    await cache.delete_value(
        key=BaseService.get_key_for_all_datas('submenus', menu_id)
    )
    await cache.delete_value(
        key=BaseService.get_key_for_all_datas('menus')
    )
