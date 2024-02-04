"""Добавить автоматическое подтягивание количества блюд и сабменю

Revision ID: 3d1909705403
Revises: 50cf3dd1c576
Create Date: 2024-01-27 13:21:48.171894

"""
from typing import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '3d1909705403'
down_revision: str | None = '50cf3dd1c576'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('menu', 'dishes_count')
    op.drop_column('menu', 'submenus_count')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('menu', sa.Column('submenus_count', sa.INTEGER(), autoincrement=False, nullable=False))
    op.add_column('menu', sa.Column('dishes_count', sa.INTEGER(), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
