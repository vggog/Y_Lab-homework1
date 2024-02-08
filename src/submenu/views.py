from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from src.core.openapi_tags import Tags

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
    description='Список всех подменю, принадлежащих меню.',
    tags=[Tags.submenus],
)
async def get_all_submenus(
        menu_id: str,
        service=Depends(Service),
) -> list[SubmenuSchema]:
    return await service.get_all_submenu(menu_id)


@submenus_router.get(
    '/{submenu_id}',
    response_model=SubmenuSchema,
    status_code=status.HTTP_200_OK,
    summary='Определённое подменю',
    tags=[Tags.submenus],
    responses={404: {'detail': {'submenu not found'}}},
)
async def get_submenu(
        submenu_id: str,
        service=Depends(Service),
) -> SubmenuSchema:
    submenu = await service.get_submenu(submenu_id=submenu_id)
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
    summary='Создать подменю',
    tags=[Tags.submenus],
)
async def create_submenu(
        menu_id: str,
        created_submenu: CreateSubmenuSchema,
        service=Depends(Service),
) -> SubmenuSchema:
    return await service.create_submenu(
        menu_id=menu_id,
        created_submenu=created_submenu
    )


@submenus_router.patch(
    '/{submenu_id}',
    response_model=SubmenuSchema,
    status_code=status.HTTP_200_OK,
    summary='Обновить подменю',
    tags=[Tags.submenus],
    responses={404: {'detail': {'submenu not found'}}},
)
async def update_submenu(
        submenu_id: str,
        updated_submenu: UpdateSubmenuSchema,
        service=Depends(Service),
):
    updated_submenu = await service.update_submenu(
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
    tags=[Tags.submenus],
)
async def delete_submenu(
        menu_id: str,
        submenu_id: str,
        service=Depends(Service),
):
    await service.delete_submenu(menu_id=menu_id, submenu_id=submenu_id)
