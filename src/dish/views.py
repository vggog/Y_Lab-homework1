from fastapi import APIRouter, Depends
from starlette import status

from .service import Service
from .schemas import DishSchema, CreateDishSchema


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
