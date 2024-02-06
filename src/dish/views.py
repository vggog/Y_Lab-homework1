from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from src.core.openapi_tags import Tags

from .schemas import CreateDishSchema, DishSchema, UpdateDishSchema
from .service import Service

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
def get_all_dishes(
        submenu_id: str,
        service=Depends(Service),
) -> list[DishSchema]:
    return service.get_all_dishes(submenu_id=submenu_id)


@dish_router.get(
    '/{dish_id}',
    response_model=DishSchema,
    status_code=status.HTTP_200_OK,
    summary='Определённое блюдо',
    tags=[Tags.dishes],
    responses={404: {'detail': {'dish not found'}}},
)
def get_dish(
        dish_id: str,
        service=Depends(Service),
) -> DishSchema:
    dish = service.get_dish(dish_id)
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
def create_dish(
        menu_id: str,
        submenu_id: str,
        created_dish: CreateDishSchema,
        service=Depends(Service),
) -> DishSchema:
    return service.create_dish(
        menu_id=menu_id,
        submenu_id=submenu_id,
        created_dish=created_dish,
    )


@dish_router.patch(
    '/{dish_id}',
    response_model=DishSchema,
    status_code=status.HTTP_200_OK,
    summary='Обновить блюдо',
    tags=[Tags.dishes],
    responses={404: {'detail': {'dish not found'}}},
)
def update_dish(
        dish_id: str,
        updated_dish: UpdateDishSchema,
        service=Depends(Service),
) -> DishSchema:
    dish = service.update_dish(
        dish_id=dish_id, updated_data=updated_dish
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
def delete_dish(
        menu_id: str,
        submenu_id: str,
        dish_id: str,
        service=Depends(Service),
):
    service.delete_dish(
        menu_id=menu_id,
        submenu_id=submenu_id,
        dish_id=dish_id,
    )
