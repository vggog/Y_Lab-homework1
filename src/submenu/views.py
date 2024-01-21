from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from .service import Service
from .schemas import SubmenuSchema, CreateSubmenuSchema, UpdateSubmenuSchema


submenus_router = APIRouter(
    prefix='/{menu_id}/submenus',
)


@submenus_router.get(
    "/",
    response_model=list[SubmenuSchema],
    status_code=status.HTTP_200_OK
)
def get_all_submenus(
        menu_id: str,
        service=Depends(Service),
):
    return service.get_all_submenu(menu_id)


@submenus_router.get(
    "/{submenu_id}",
    response_model=SubmenuSchema,
    status_code=status.HTTP_200_OK
)
def get_submenu(
        submenu_id: str,
        menu_id: str,
        service=Depends(Service),
):
    submenu = service.get_submenu(submenu_id=submenu_id, menu_id=menu_id)
    if submenu is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="submenu not found",
        )

    return submenu


@submenus_router.post(
    "/",
    response_model=SubmenuSchema,
    status_code=status.HTTP_201_CREATED,
)
def create_submenu(
        menu_id: str,
        created_submenu: CreateSubmenuSchema,
        service=Depends(Service),
):
    return service.create_submenu(
        menu_id=menu_id,
        created_submenu=created_submenu
    )


@submenus_router.patch(
    "/{submenu_id}",
    response_model=SubmenuSchema,
    status_code=status.HTTP_200_OK,
)
def update_submenu(
        submenu_id: str,
        updated_submenu: UpdateSubmenuSchema,
        service=Depends(Service),
):
    updated_submenu = service.update_submenu(
        submenu_id=submenu_id,
        updated_data=updated_submenu
    )

    if updated_submenu is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="submenu not found",
        )

    return updated_submenu
