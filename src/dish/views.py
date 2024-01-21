from fastapi import APIRouter, Depends
from starlette import status

from .service import Service
from .schemas import DishSchema


dish_router = APIRouter(
    prefix='/menus/{menu_id}/submenus/{submenu_id}/dishes',
)


@dish_router.get(
    "/",
    response_model=list[DishSchema],
    status_code=status.HTTP_200_OK
)
def get_all_submenus(
        service=Depends(Service),
):
    return service.get_all_dishes()
