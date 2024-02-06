from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from src.core.openapi_tags import Tags

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
    tags=[Tags.menus],
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
    tags=[Tags.menus],
    responses={404: {'detail': {'menu not found'}}},
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
    tags=[Tags.menus],
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
    tags=[Tags.menus],
    responses={404: {'detail': {'menu not found'}}},
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
    tags=[Tags.menus],
)
def delete_menu(
        menu_id: str,
        service=Depends(Service),
):
    service.delete_menu(menu_id)
