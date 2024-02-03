from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from .schemas import CreateDishSchema, DishSchema, UpdateDishSchema
from .service import Service

dish_router = APIRouter(
    prefix='/menus/{menu_id}/submenus/{submenu_id}/dishes',
)


@dish_router.get(
    '/',
    response_model=list[DishSchema],
    status_code=status.HTTP_200_OK
)
def get_all_dishes(
        service=Depends(Service),
):
    return service.get_all_dishes()


@dish_router.get(
    '/{dish_id}',
    response_model=DishSchema,
    status_code=status.HTTP_200_OK,
)
def get_dish(
        dish_id: str,
        service=Depends(Service),
):
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
)
def create_dish(
        menu_id: str,
        submenu_id: str,
        created_dish: CreateDishSchema,
        service=Depends(Service),
):
    return service.create_dish(
        menu_id=menu_id,
        submenu_id=submenu_id,
        created_dish=created_dish,
    )


@dish_router.patch(
    '/{dish_id}',
    response_model=DishSchema,
    status_code=status.HTTP_200_OK,
)
def update_dish(
        dish_id: str,
        updated_dish: UpdateDishSchema,
        service=Depends(Service),
):
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
