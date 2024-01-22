from sqlalchemy.orm import Mapped, relationship

from src.core.model import BaseModel

from src.submenu.model import SubmenuModel


class MenuModel(BaseModel):
    __tablename__ = "menu"

    submenus: Mapped[list["SubmenuModel"]] = relationship(
        back_populates="menu",
        cascade="all, delete",
        passive_deletes=True,
    )
