from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from .schemas import CreateSubmenuSchema, SubmenuSchema, UpdateSubmenuSchema
from .service import Service

submenus_router = APIRouter(
    prefix='/{menu_id}/submenus',
)


@submenus_router.get(
    '/',
    response_model=list[SubmenuSchema],
    status_code=status.HTTP_200_OK,
    summary='Список всех подменю',
    description='Список всех подменю, принадлежащих меню.'
)
def get_all_submenus(
        menu_id: str,
        service=Depends(Service),
) -> list[SubmenuSchema]:
    return service.get_all_submenu(menu_id)


@submenus_router.get(
    '/{submenu_id}',
    response_model=SubmenuSchema,
    status_code=status.HTTP_200_OK,
    summary='Определённое подменю',
)
def get_submenu(
        submenu_id: str,
        service=Depends(Service),
) -> SubmenuSchema:
    submenu = service.get_submenu(submenu_id=submenu_id)
    if submenu is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='submenu not found',
        )

    return submenu


@submenus_router.post(
    '/',
    response_model=SubmenuSchema,
    status_code=status.HTTP_201_CREATED,
    summary='Создать подменю'
)
def create_submenu(
        menu_id: str,
        created_submenu: CreateSubmenuSchema,
        service=Depends(Service),
) -> SubmenuSchema:
    return service.create_submenu(
        menu_id=menu_id,
        created_submenu=created_submenu
    )


@submenus_router.patch(
    '/{submenu_id}',
    response_model=SubmenuSchema,
    status_code=status.HTTP_200_OK,
    summary='Обновить подменю'
)
def update_submenu(
        submenu_id: str,
        updated_submenu: UpdateSubmenuSchema,
        service=Depends(Service),
) -> SubmenuSchema:
    updated_submenu = service.update_submenu(
        submenu_id=submenu_id,
        updated_data=updated_submenu
    )

    if updated_submenu is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='submenu not found',
        )

    return updated_submenu


@submenus_router.delete(
    '/{submenu_id}',
    status_code=status.HTTP_200_OK,
    summary='Удалить подменю',
    description='При удаление подменю, '
                'так-же удаляются все блюда, принадлежащих меню.',
)
def delete_submenu(
        menu_id: str,
        submenu_id: str,
        service=Depends(Service),
):
    service.delete_submenu(menu_id=menu_id, submenu_id=submenu_id)
