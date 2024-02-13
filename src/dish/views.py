from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from starlette import status

from src.core.openapi_tags import Tags
from src.dish.model import DishModel
from src.dish.schemas import CreateDishSchema, DishSchema, UpdateDishSchema
from src.dish.service import Service

dish_router = APIRouter(
    prefix='/menus/{menu_id}/submenus/{submenu_id}/dishes',
)


@dish_router.get(
    '/',
    response_model=list[DishSchema],
    status_code=status.HTTP_200_OK,
    summary='Список всех блюд',
    description='Список всех блюда, принадлежащих определённому подменю.',
    tags=[Tags.dishes],
)
async def get_all_dishes(
        submenu_id: str,
        background_tasks: BackgroundTasks,
        service=Depends(Service),
) -> list[DishModel]:
    return await service.get_all_dishes(
        submenu_id=submenu_id,
        background_tasks=background_tasks,
    )


@dish_router.get(
    '/{dish_id}',
    response_model=DishSchema,
    status_code=status.HTTP_200_OK,
    summary='Определённое блюдо',
    tags=[Tags.dishes],
    responses={404: {'detail': {'dish not found'}}},
)
async def get_dish(
        dish_id: str,
        background_tasks: BackgroundTasks,
        service=Depends(Service),
) -> DishModel:
    dish: DishModel | None = await service.get_dish(
        dish_id,
        background_tasks=background_tasks,
    )
    if dish is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='dish not found',
        )

    return dish


@dish_router.post(
    '/',
    response_model=DishSchema,
    status_code=status.HTTP_201_CREATED,
    summary='Создать блюдо',
    tags=[Tags.dishes],
)
async def create_dish(
        menu_id: str,
        submenu_id: str,
        background_tasks: BackgroundTasks,
        created_dish: CreateDishSchema,
        service=Depends(Service),
) -> DishModel:
    return await service.create_dish(
        menu_id=menu_id,
        submenu_id=submenu_id,
        created_dish=created_dish,
        background_tasks=background_tasks,
    )


@dish_router.patch(
    '/{dish_id}',
    response_model=DishSchema,
    status_code=status.HTTP_200_OK,
    summary='Обновить блюдо',
    tags=[Tags.dishes],
    responses={404: {'detail': {'dish not found'}}},
)
async def update_dish(
        dish_id: str,
        updated_dish: UpdateDishSchema,
        background_tasks: BackgroundTasks,
        service=Depends(Service),
) -> DishModel:
    dish: DishModel | None = await service.update_dish(
        dish_id=dish_id,
        updated_data=updated_dish,
        background_tasks=background_tasks,
    )
    if dish is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='dish not found',
        )

    return dish


@dish_router.delete(
    '/{dish_id}',
    status_code=status.HTTP_200_OK,
    summary='Удалить блюдо',
    tags=[Tags.dishes],
)
async def delete_dish(
        menu_id: str,
        submenu_id: str,
        dish_id: str,
        background_tasks: BackgroundTasks,
        service=Depends(Service),
) -> None:
    await service.delete_dish(
        menu_id=menu_id,
        submenu_id=submenu_id,
        dish_id=dish_id,
        background_tasks=background_tasks,
    )
