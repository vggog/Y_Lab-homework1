from openpyxl.worksheet.worksheet import Worksheet

from src.tasks.schemas import Dish, Menu, RowData, Submenu


class ParseExcel:
    menus: list[Menu] = []
    submenus: list[Submenu] = []
    dishes: list[Dish] = []

    def __init__(self, sheet: Worksheet):
        self.sheet = sheet
        self.rows_count = sheet.max_row

    def _get_column_datas(self, row: int) -> RowData:
        """Получить данные строки"""
        return RowData(
            a_column=self.sheet[f'A{row}'].value,
            b_column=self.sheet[f'B{row}'].value,
            c_column=self.sheet[f'C{row}'].value,
            d_column=self.sheet[f'D{row}'].value,
            e_column=self.sheet[f'E{row}'].value,
            f_column=self.sheet[f'F{row}'].value,
            g_column=self.sheet[f'G{row}'].value,
        )

    @staticmethod
    def _is_menus_datas(row_data: RowData) -> bool:
        """Проверка, наличия данных для меню"""
        return (row_data.a_column is not None) and (
            row_data.b_column is not None) and (
            row_data.c_column is not None)

    @staticmethod
    def _is_submenus_datas(row_data: RowData) -> bool:
        """Проверка, наличия данных для подменю"""
        return (
            (row_data.b_column is not None) and (row_data.c_column is not None) and (row_data.d_column is not None)
        )

    @staticmethod
    def _is_dishes_datas(row_data: RowData) -> bool:
        """Проверка, наличия данных для блюда"""
        return (
            (row_data.c_column is not None) and (row_data.d_column is not None) and (
                row_data.e_column is not None) and (row_data.f_column is not None)
        )

    def _get_menu_datas(self, row_data: RowData) -> Menu:
        """Получить данные о меню"""
        return Menu(
            id_=row_data.a_column,
            title=row_data.b_column,
            description=row_data.c_column,
            submenus=self.submenus
        )

    def _get_submenu_datas(self, row_data: RowData) -> Submenu:
        """Получить данные о подменю"""
        return Submenu(
            id_=row_data.b_column,
            title=row_data.c_column,
            description=row_data.d_column,
            dishes=self.dishes,
        )

    @staticmethod
    def _get_dish_datas(row_data: RowData) -> Dish:
        """Получить данные о блюде"""
        return Dish(
            id_=row_data.c_column,
            title=row_data.d_column,
            description=row_data.e_column,
            price=float(row_data.f_column),
            discount=int(row_data.g_column) if row_data.g_column else 0,
        )

    def parse(self) -> list[Menu]:
        """Получить данные из таблицы"""
        for row in range(self.rows_count, 0, -1):
            row_data: RowData = self._get_column_datas(row)

            if self._is_dishes_datas(row_data):
                self.dishes.append(self._get_dish_datas(row_data))
            elif self._is_submenus_datas(row_data):
                self.submenus.append(self._get_submenu_datas(row_data))
                self.dishes = []
            elif self._is_menus_datas(row_data):
                self.menus.append(self._get_menu_datas(row_data))
                self.submenus = []

        return self.menus
