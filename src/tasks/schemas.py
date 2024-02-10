from dataclasses import dataclass


@dataclass
class Dish:
    id_: str
    title: str
    description: str
    price: float
    discount: int


@dataclass
class Submenu:
    id_: str
    title: str
    description: str
    dishes: list[Dish]


@dataclass
class Menu:
    id_: str
    title: str
    description: str
    submenus: list[Submenu]


@dataclass
class RowData:
    a_column: str  # id меню
    b_column: str  # название меню или id подменю
    c_column: str  # описание меню или название подменю или id блюда
    d_column: str  # описание подменю или название блюда
    e_column: str  # описание блюда
    f_column: str  # цена блюда
    g_column: str  # скидка на блюдо
