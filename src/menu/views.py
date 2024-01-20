from fastapi import APIRouter, Depends

from .service import Service
from .schemas import MenuSchema


menus_router = APIRouter(
    prefix='/menus',
)


@menus_router.get(
    "/",
    response_model=list[MenuSchema]
)
def get_all_menus(
        service=Depends(Service),
):
    return service.get_all_menus()
