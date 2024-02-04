from sqlalchemy.orm import Session

from src.core.repository import BaseRepository
from src.dish.model import DishModel
from src.menu.model import MenuModel
from src.submenu.model import SubmenuModel


class Repository(BaseRepository):
    _model = MenuModel

    def get_all_dishes(self, menu_id: str) -> list[DishModel]:
        """Метод для получения всех блюд, принадлежащих меню"""
        with Session(self.engine) as session:
            return (
                session.query(
                    DishModel
                ).filter(
                    MenuModel.id == SubmenuModel.menu_id
                ).filter(
                    SubmenuModel.id == DishModel.submenu_id
                ).filter(
                    MenuModel.id == menu_id
                ).all()
            )
