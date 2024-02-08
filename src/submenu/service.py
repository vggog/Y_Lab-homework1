from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.core.cache import Cache
from src.core.db_session import get_db_session
from src.core.service import BaseService
from src.submenu.model import SubmenuModel
from src.submenu.repository import Repository
from src.submenu.schemas import CreateSubmenuSchema, SubmenuSchema, UpdateSubmenuSchema


class Service(BaseService):

    def __init__(
            self,
            repository=Depends(Repository),
            cache=Depends(Cache),
            async_session: async_sessionmaker[AsyncSession] = Depends(
                get_db_session
            ),
    ):
        self.async_session = async_session
        self.repository = repository
        self.cache = cache

    async def get_all_submenu(
            self,
            menu_id: str
    ) -> list[SubmenuModel] | list[dict[str, str]]:
        key = self.get_key_for_all_datas('submenus', menu_id)
        all_submenus_from_cache = await self.cache.get_value(key)
        if all_submenus_from_cache is not None:
            return all_submenus_from_cache

        all_submenus: list[SubmenuModel] = await self.repository.get_all(
            menu_id=menu_id,
            async_session=self.async_session,
        )

        await self.cache.set_list_of_values(
            key=key,
            datas=all_submenus,
            schema=SubmenuSchema,
        )

        return all_submenus

    async def get_submenu(
            self,
            submenu_id: str
    ) -> SubmenuModel | dict[str, str] | None:
        """Сервис для получения подменю."""
        submenu_from_cache: dict[str, str] = await self.cache.get_value(
            submenu_id
        )
        if submenu_from_cache is not None:
            return submenu_from_cache

        submenu: SubmenuModel = await self.repository.get(
            id=submenu_id,
            async_session=self.async_session,
        )
        if submenu is None:
            return None

        await self.cache.set_value(
            key=submenu.id,
            data=submenu,
            schema=SubmenuSchema,
        )

        return submenu

    async def create_submenu(
            self,
            menu_id: str,
            created_submenu: CreateSubmenuSchema
    ) -> SubmenuModel:
        """
        Метод для создания меню.
        Созданное меню добавляется в кэш.
        """
        submenu: SubmenuModel = await self.repository.create(
            menu_id=menu_id,
            async_session=self.async_session,
            **created_submenu.model_dump(),
        )
        await self.cache.set_value(
            key=submenu.id,
            data=submenu,
            schema=SubmenuSchema,
        )
        await self.cache.delete_value(menu_id)
        await self.cache.delete_value(
            key=self.get_key_for_all_datas('submenus', menu_id)
        )
        await self.cache.delete_value(
            key=self.get_key_for_all_datas('menus')
        )

        return submenu

    async def update_submenu(
            self,
            submenu_id: str,
            updated_data: UpdateSubmenuSchema,
    ) -> SubmenuModel | None:
        """
        Сервис для обновления подменю.
        Данные о подменю обновляются в кэше.
        """
        updated_data_dict: dict[str, str] = self.delete_non_value_key(
            updated_data.model_dump()
        )

        await self.cache.delete_value(submenu_id)

        submenu: SubmenuModel | None = await self.repository.update(
            submenu_id,
            async_session=self.async_session,
            **updated_data_dict
        )

        if submenu is not None:
            await self.cache.set_value(
                key=submenu.id,
                data=submenu,
                schema=SubmenuSchema,
            )
        return submenu

    async def delete_submenu(self, menu_id: str, submenu_id: str):
        """Сервис для удаления подменю."""
        await self.cache.delete_value(menu_id)
        await self.cache.delete_value(submenu_id)
        await self.cache.delete_value(
            key=self.get_key_for_all_datas('submenus', menu_id)
        )
        await self.cache.delete_value(
            key=self.get_key_for_all_datas('menus')
        )

        await self.repository.delete(
            submenu_id,
            async_session=self.async_session,
        )
