from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from .schemas import CreateMenuSchema, MenuSchema, UpdateMenuSchema
from .service import Service

menus_router = APIRouter(
    prefix='/menus',
)


@menus_router.get(
    '/',
    response_model=list[MenuSchema],
    status_code=status.HTTP_200_OK,
    summary='Список всех меню',
)
def get_all_menus(
        service=Depends(Service),
) -> list[MenuSchema]:
    return service.get_all_menus()


@menus_router.get(
    '/{menu_id}',
    response_model=MenuSchema,
    status_code=status.HTTP_200_OK,
    summary='Конкретное меню',
)
def get_menu_by_id(
        menu_id: str,
        service=Depends(Service),
) -> MenuSchema:
    menu = service.get_menu(menu_id)

    if menu is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='menu not found',
        )

    return menu


@menus_router.post(
    '/',
    response_model=MenuSchema,
    status_code=status.HTTP_201_CREATED,
    summary='Создать меню',
)
def create_menu(
        created_menu: CreateMenuSchema,
        service=Depends(Service),
) -> MenuSchema:
    return service.create_menu(created_menu)


@menus_router.patch(
    '/{menu_id}',
    response_model=MenuSchema,
    status_code=status.HTTP_200_OK,
    summary='Обновить меню',
)
def update_menu(
        menu_id: str,
        update_menu_data: UpdateMenuSchema,
        service=Depends(Service),
) -> MenuSchema:
    updated_menu = service.update_menu(menu_id, update_menu_data)
    if updated_menu is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='menu not found',
        )

    return updated_menu


@menus_router.delete(
    '/{menu_id}',
    status_code=status.HTTP_200_OK,
    summary='Удалить меню',
    description='При удаление меню, '
                'также удаляются все подменю и блюда принадлежащие меню',
)
def delete_menu(
        menu_id: str,
        service=Depends(Service),
):
    service.delete_menu(menu_id)
