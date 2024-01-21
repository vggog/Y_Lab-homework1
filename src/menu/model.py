from sqlalchemy.orm import Mapped, relationship

from src.core.model import BaseModel

from src.submenu.model import SubmenuModel


class MenuModel(BaseModel):
    __tablename__ = "menu"

    submenus: Mapped[list["SubmenuModel"]] = relationship(
        cascade="all, delete"
    )
