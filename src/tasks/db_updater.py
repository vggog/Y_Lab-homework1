import requests

from src.core.config import app_config
from src.tasks.schemas import Dish, Menu, Submenu


class DataBaseUpdater:
    datas: list[Menu]

    def __init__(self, datas: list[Menu]):
        self.datas = datas

    def _has_update(self, data: dict, new_data: dict) -> bool:
        """Метод для проверки надобности обновления данных."""
        return data != new_data

    def create_or_update(
            self,
            entity_id: str,
            entity_url: str,
            entity_data: dict[str, str]
    ) -> str:
        """
        Создать сущность, если она не создана.
        Обновить сущность, если данные устарели.
        """
        response = requests.get(f'{entity_url}/{entity_id}')

        if response.status_code == 200:
            if self._has_update(response.json(), entity_data):
                response = requests.patch(
                    f'{entity_url}/{entity_id}',
                    json=entity_data,
                )

            return response.json()['id']
        elif response.status_code == 404:
            response = requests.post(
                entity_url,
                json=entity_data,
            )

            return response.json()['id']
        else:
            raise Exception(
                'Ошибка сервера: ',
                response.status_code
            )

    def check_menu(self, menu: Menu) -> str:
        """
        Проверка меню.
        Удаляет подменю, не присутствующие в базе экселя.
        """
        menu_id = self.create_or_update(
            entity_id=menu.id_,
            entity_url=app_config.url_prefix + app_config.menus_postfix,
            entity_data={
                'title': menu.title,
                'description': menu.description,
            },
        )

        submenus_id: list[str] = []
        for submenu in menu.submenus:
            submenu_id = self.check_submenu(menu_id, submenu)
            submenus_id.append(submenu_id)

        self.delete_entitys(
            url=app_config.url_prefix + app_config.submenus_postfix.format(
                menu_id=menu_id,
            ),
            entity_ids=submenus_id,
        )

        return menu_id

    def check_submenu(self, menu_id: str, submenu: Submenu) -> str:
        """
        Проверка подменю.
        Удаляет блюда, которых нет в обновлённой базе.
        """
        url = app_config.url_prefix + app_config.submenus_postfix.format(
            menu_id=menu_id,
        )
        submenu_id = self.create_or_update(
            entity_id=submenu.id_,
            entity_url=url,
            entity_data={
                'title': submenu.title,
                'description': submenu.description,
            },
        )

        dishes_id: list[str] = []
        for dish in submenu.dishes:
            dish_id = self.check_dish(
                menu_id=menu_id,
                submenu_id=submenu_id,
                dish=dish,
            )
            dishes_id.append(dish_id)

        self.delete_entitys(
            url=app_config.url_prefix + app_config.dishes_postfix.format(
                menu_id=menu_id,
                submenu_id=submenu_id,
            ),
            entity_ids=dishes_id,
        )

        return submenu_id

    def check_dish(self, menu_id: str, submenu_id: str, dish: Dish) -> str:
        """
        Проверка блюда.
        :param menu_id:
        :param submenu_id:
        :param dish:
        :return:
        """
        url = app_config.url_prefix + app_config.dishes_postfix.format(
            menu_id=menu_id,
            submenu_id=submenu_id,
        )
        return self.create_or_update(
            entity_id=dish.id_,
            entity_url=url,
            entity_data={
                'title': dish.title,
                'description': dish.description,
                'price': str(dish.price),
            },
        )

    def delete_entitys(
            self,
            url: str,
            entity_ids: list[str],
    ) -> None:
        """
        Удалить сущность, которой нет в обновлённой базе.
        """
        response = requests.get(url)
        db_entity_id = [entity['id'] for entity in response.json()]

        for entity_id in db_entity_id:
            if entity_id not in entity_ids:
                requests.delete(
                    f'{app_config.url_prefix + app_config.menus_postfix}/{entity_id}'
                )

    def run(self) -> None:
        menus_id: list[str] = []
        for menu in self.datas:
            menu_id = self.check_menu(menu)
            menus_id.append(menu_id)

        self.delete_entitys(
            url=app_config.url_prefix + app_config.menus_postfix,
            entity_ids=menus_id,
        )
