from fastapi import APIRouter, Depends, HTTPException
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


@menus_router.get(
    "/{menu_id}",
    response_model=MenuSchema,
)
def get_menu_by_id(
        menu_id: int,
        service=Depends(Service),
):
    menu = service.get_menu(menu_id)

    if menu is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
        )

    return menu


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
