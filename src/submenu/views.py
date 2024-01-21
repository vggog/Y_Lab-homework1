from fastapi import APIRouter, Depends
from starlette import status

from .service import Service
from .schemas import SubmenuSchema


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
