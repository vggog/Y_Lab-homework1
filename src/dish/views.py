from fastapi import APIRouter, Depends
from starlette import status

from .service import Service
from .schemas import DishSchema, CreateDishSchema, UpdateDishSchema


dish_router = APIRouter(
    prefix='/menus/{menu_id}/submenus/{submenu_id}/dishes',
)


@dish_router.get(
    "/",
    response_model=list[DishSchema],
    status_code=status.HTTP_200_OK
)
def get_all_dishes(
        service=Depends(Service),
):
    return service.get_all_dishes()


@dish_router.get(
    "/{dish_id}",
    response_model=DishSchema,
    status_code=status.HTTP_200_OK,
)
def get_dish(
        dish_id: str,
        service=Depends(Service),
):
    return service.get_dish(dish_id)


@dish_router.post(
    "/",
    response_model=DishSchema,
    status_code=status.HTTP_201_CREATED,
)
def create_dish(
        submenu_id: str,
        created_dish: CreateDishSchema,
        service=Depends(Service),
):
    return service.create_dish(
        submenu_id=submenu_id, created_dish=created_dish
    )


@dish_router.patch(
    "/{dish_id}",
    response_model=DishSchema,
    status_code=status.HTTP_200_OK,
)
def update_dish(
        dish_id: str,
        updated_dish: UpdateDishSchema,
        service=Depends(Service),
):
    return service.update_dish(
        dish_id=dish_id, updated_data=updated_dish
    )


@dish_router.delete(
    "/{dish_id}",
    status_code=status.HTTP_200_OK,
)
def delete_dish(
        dish_id: str,
        service=Depends(Service),
):
    service.delete_dish(dish_id)
