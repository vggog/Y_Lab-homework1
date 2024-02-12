from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from starlette import status

from src.core.db_session import get_db_session
from src.core.openapi_tags import Tags

from .schemas import CreateMenuSchema, MenuFullBaseSchema, MenuSchema, UpdateMenuSchema
from .service import Service

menus_router = APIRouter(
    prefix='/menus',
)


@menus_router.get(
    '/fullbase',
    response_model=list[MenuFullBaseSchema],
    status_code=status.HTTP_200_OK,
    summary='Список всех меню, со связанными подменю, со связанными блюдами',
    tags=[Tags.menus],
)
async def full_base(
        background_tasks: BackgroundTasks,
        service=Depends(Service),
        async_session=Depends(get_db_session),
):
    return await service.full_base(
        background_tasks=background_tasks,
        async_session=async_session
    )


@menus_router.get(
    '/',
    response_model=list[MenuSchema],
    status_code=status.HTTP_200_OK,
    summary='Список всех меню',
    tags=[Tags.menus],
)
async def get_all_menus(
        background_tasks: BackgroundTasks,
        service=Depends(Service),
        async_session=Depends(get_db_session),
) -> list[MenuSchema]:
    return await service.get_all_menus(
        async_session=async_session,
        background_tasks=background_tasks,
    )


@menus_router.get(
    '/{menu_id}',
    response_model=MenuSchema,
    status_code=status.HTTP_200_OK,
    summary='Конкретное меню',
    tags=[Tags.menus],
    responses={404: {'detail': {'menu not found'}}},
)
async def get_menu_by_id(
        menu_id: str,
        background_tasks: BackgroundTasks,
        service=Depends(Service),
        async_session=Depends(get_db_session),
) -> MenuSchema:
    menu = await service.get_menu(
        menu_id,
        async_session=async_session,
        background_tasks=background_tasks,
    )

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
async def create_menu(
        created_menu: CreateMenuSchema,
        background_tasks: BackgroundTasks,
        service=Depends(Service),
        async_session=Depends(get_db_session),
) -> MenuSchema:
    return await service.create_menu(
        created_menu,
        async_session=async_session,
        background_tasks=background_tasks,
    )


@menus_router.patch(
    '/{menu_id}',
    response_model=MenuSchema,
    status_code=status.HTTP_200_OK,
    summary='Обновить меню',
    tags=[Tags.menus],
    responses={404: {'detail': {'menu not found'}}},
)
async def update_menu(
        menu_id: str,
        update_menu_data: UpdateMenuSchema,
        background_tasks: BackgroundTasks,
        service=Depends(Service),
        async_session=Depends(get_db_session),
) -> MenuSchema:
    updated_menu = await service.update_menu(
        menu_id,
        update_menu_data,
        async_session=async_session,
        background_tasks=background_tasks,
    )
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
async def delete_menu(
        menu_id: str,
        background_tasks: BackgroundTasks,
        service=Depends(Service),
        async_session=Depends(get_db_session),
):
    await service.delete_menu(
        menu_id,
        async_session=async_session,
        background_tasks=background_tasks,
    )
