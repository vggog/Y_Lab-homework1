from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.model import BaseModel


class DishModel(BaseModel):
    __tablename__ = "dish"

    price: Mapped[str]
    submenu_id: Mapped[str] = mapped_column(
        ForeignKey(
            "submenu.id",
            ondelete="CASCADE"
        )
    )
    submenu: Mapped["SubmenuModel"] = relationship(
        back_populates="dishes",
        cascade="all, delete",
    )
