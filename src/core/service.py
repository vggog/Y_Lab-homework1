class BaseService:

    @staticmethod
    def delete_non_value_key(data: dict[str, str | None]) -> dict[str, str]:
        """Метод для удаления ключей со значениями None"""
        updated_dict: dict[str, str] = {
            k: v for k, v in data.items() if v is not None
        }

        return updated_dict

    @staticmethod
    def get_key_for_all_datas(category: str, id_: str = '') -> str:
        """

        :param category: Категория сущносности для списка.
                Может быть только menus, submenus, diches, full_base.
        :param id_: id родительской сущности.
                Для submenu - menu_id
                Для dish - submenu_id
        :return ключ для redis:
        """
        if category not in ('menus', 'submenus', 'dishes', 'full_base'):
            raise TypeError(
                'Категория для создания ключа должен быть: '
                'menus, submenus, diches, full_base'
            )

        key = ''
        if id_:
            key += id_ + '_'

        key += f'all_{category}'

        return key
