from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from starlette import status

from src.core.openapi_tags import Tags
from src.submenu.model import SubmenuModel
from src.submenu.schemas import CreateSubmenuSchema, SubmenuSchema, UpdateSubmenuSchema
from src.submenu.service import Service

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
        background_tasks: BackgroundTasks,
        service=Depends(Service),
) -> list[SubmenuModel]:
    return await service.get_all_submenu(
        menu_id,
        background_tasks=background_tasks,
    )


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
        background_tasks: BackgroundTasks,
        service=Depends(Service),
) -> SubmenuModel:
    submenu: SubmenuModel | None = await service.get_submenu(
        submenu_id=submenu_id,
        background_tasks=background_tasks,
    )
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
        background_tasks: BackgroundTasks,
        service=Depends(Service),
) -> SubmenuModel:
    return await service.create_submenu(
        menu_id=menu_id,
        created_submenu=created_submenu,
        background_tasks=background_tasks,
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
        to_update_submenu: UpdateSubmenuSchema,
        background_tasks: BackgroundTasks,
        service=Depends(Service),
) -> SubmenuModel:
    updated_submenu: SubmenuModel | None = await service.update_submenu(
        submenu_id=submenu_id,
        updated_data=to_update_submenu,
        background_tasks=background_tasks,
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
        background_tasks: BackgroundTasks,
        service=Depends(Service),
) -> None:
    await service.delete_submenu(
        menu_id=menu_id,
        submenu_id=submenu_id,
        background_tasks=background_tasks,
    )
