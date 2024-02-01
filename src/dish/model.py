from uuid import uuid4

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.model import BaseModel


class DishModel(BaseModel):
    __tablename__ = "dish"

    id: Mapped[str] = mapped_column(
        primary_key=True,
        default=lambda: str(uuid4()),
    )

    price: Mapped[str]
    submenu_id: Mapped[str] = mapped_column(
        ForeignKey(
            "submenu.id",
            ondelete="CASCADE"
        )
    )
    submenu = relationship(
        "SubmenuModel",
        back_populates="dishes",
        cascade="all, delete",
    )
