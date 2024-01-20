from fastapi import APIRouter, Depends
from starlette import status

from .service import Service
from .schemas import MenuSchema, CreateMenuSchema


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


@menus_router.post(
    "/",
    response_model=MenuSchema,
    status_code=status.HTTP_201_CREATED,
)
def create_menu(
        created_menu: CreateMenuSchema,
        service=Depends(Service),
):
    return service.create_menu(created_menu)
