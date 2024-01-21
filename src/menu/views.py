from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from .service import Service
from .schemas import MenuSchema, CreateMenuSchema, UpdateMenuSchema


menus_router = APIRouter(
    prefix='/menus',
)


@menus_router.get(
    "/",
    response_model=list[MenuSchema],
    status_code=status.HTTP_200_OK
)
def get_all_menus(
        service=Depends(Service),
):
    return service.get_all_menus()


@menus_router.get(
    "/{menu_id}",
    response_model=MenuSchema,
    status_code=status.HTTP_200_OK
)
def get_menu_by_id(
        menu_id: str,
        service=Depends(Service),
):
    menu = service.get_menu(menu_id)

    if menu is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="menu not found",
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


@menus_router.patch(
    "/{menu_id}",
    response_model=MenuSchema,
    status_code=status.HTTP_200_OK,
)
def update_menu(
        menu_id: str,
        update_menu_data: UpdateMenuSchema,
        service=Depends(Service),
):
    updated_menu = service.update_menu(menu_id, update_menu_data)
    if updated_menu is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="menu not found",
        )

    return updated_menu


@menus_router.delete(
    "/{menu_id}",
    status_code=status.HTTP_200_OK
)
def delete_menu(
        menu_id: str,
        service=Depends(Service),
):
    service.delete_menu(menu_id)
