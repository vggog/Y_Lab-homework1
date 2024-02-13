from src.core.db_session import get_db_session
from src.core.repository import BaseRepository
from src.dish.repository import Repository as DishRepository
from src.menu.repository import Repository as MenuRepository
from src.submenu.repository import Repository as SubmenuRepository
from src.tasks.schemas import Dish, Menu, Submenu


class DataBaseUpdater:
    datas: list[Menu]

    def __init__(self, datas: list[Menu]):
        self.datas = datas

    @staticmethod
    def _has_update(data: dict, new_data: dict) -> bool:
        """Метод для проверки надобности обновления данных."""
        for key_of_new_data in new_data.keys():
            if new_data[key_of_new_data] != data[key_of_new_data]:
                return True

        return False

    async def create_or_update(
            self,
            entity_id: str,
            repository: BaseRepository,
            entity_data: dict[str, str],
    ) -> str:
        """
        Создать сущность, если она не создана.
        Обновить сущность, если данные устарели.
        """

        entity = await repository.get(
            id=str(entity_id),
            async_session=await get_db_session().__anext__(),
        )

        if entity:
            if self._has_update(entity.__dict__, entity_data):
                await repository.update(
                    object_id=str(entity_id),
                    async_session=await get_db_session().__anext__(),
                    **entity_data,
                )
        else:
            entity = await repository.create(
                async_session=await get_db_session().__anext__(),
                **entity_data,
            )

        return str(entity.id)

    async def check_menu(self, menu: Menu) -> str:
        """
        Проверка меню.
        Удаляет подменю, не присутствующие в базе экселя.
        """
        menu_id = await self.create_or_update(
            entity_id=menu.id_,
            repository=MenuRepository(),
            entity_data={
                'title': menu.title,
                'description': menu.description,
            },
        )

        submenus_id: list[str] = []
        for submenu in menu.submenus:
            submenu_id = await self.check_submenu(menu_id, submenu)
            submenus_id.append(submenu_id)

        submenu_repository = SubmenuRepository()
        all_submenus_from_db = await submenu_repository.get_all(
            menu_id=menu_id,
            async_session=await get_db_session().__anext__(),
        )

        await self.delete_entities(
            db_ids=[submenu_from_db.id for submenu_from_db in all_submenus_from_db],
            entity_ids=submenus_id,
            repository=submenu_repository,
        )

        return menu_id

    async def check_submenu(self, menu_id: str, submenu: Submenu) -> str:
        """
        Проверка подменю.
        Удаляет блюда, которых нет в обновлённой базе.
        """
        submenu_id = await self.create_or_update(
            entity_id=submenu.id_,
            repository=SubmenuRepository(),
            entity_data={
                'menu_id': menu_id,
                'title': submenu.title,
                'description': submenu.description,
            },
        )

        dishes_id: list[str] = []
        for dish in submenu.dishes:
            dish_id = await self.check_dish(
                submenu_id=submenu_id,
                dish=dish,
            )
            dishes_id.append(dish_id)

        dish_repository = DishRepository()
        all_dishes_from_db = await dish_repository.get_all(
            submenu_id=submenu_id,
            async_session=await get_db_session().__anext__(),
        )

        await self.delete_entities(
            db_ids=[dish_from_db.id for dish_from_db in all_dishes_from_db],
            entity_ids=dishes_id,
            repository=dish_repository,
        )

        return submenu_id

    async def check_dish(self, submenu_id: str, dish: Dish) -> str:
        """
        Проверка блюда.
        :param submenu_id:
        :param dish:
        :return:
        """
        return await self.create_or_update(
            entity_id=dish.id_,
            repository=DishRepository(),
            entity_data={
                'submenu_id': submenu_id,
                'title': dish.title,
                'description': dish.description,
                'price': str(dish.price),
            },
        )

    @staticmethod
    async def delete_entities(
            db_ids: list[str],
            entity_ids: list[str],
            repository: BaseRepository,
    ) -> None:
        """
        Удалить сущность, которой нет в обновлённой базе.
        """
        for entity_id in db_ids:
            if entity_id not in entity_ids:
                await repository.delete(
                    object_id=str(entity_id),
                    async_session=await get_db_session().__anext__()
                )

    async def run(self) -> None:
        menus_id: list[str] = []
        for menu in self.datas:
            menu_id = await self.check_menu(menu)
            menus_id.append(str(menu_id))

        menu_repository: MenuRepository = MenuRepository()

        datas = await menu_repository.get_all(
            await get_db_session().__anext__()
        )

        await self.delete_entities(
            db_ids=[menu_from_db.id for menu_from_db in datas],
            entity_ids=menus_id,
            repository=menu_repository,
        )
