from src.core.repository import BaseRepository
from .model import MenuModel


class Repository(BaseRepository):
    _model = MenuModel
