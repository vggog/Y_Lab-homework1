from src.core.repository import BaseRepository
from .model import DishModel


class Repository(BaseRepository):
    _model = DishModel
