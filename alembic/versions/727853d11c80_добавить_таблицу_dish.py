"""Добавить таблицу dish

Revision ID: 727853d11c80
Revises: 404fa5a9f8bd
Create Date: 2024-01-21 18:46:50.777025

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '727853d11c80'
down_revision: str | None = '404fa5a9f8bd'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('dish',
                    sa.Column('price', sa.String(), nullable=False),
                    sa.Column('submenu_id', sa.String(), nullable=False),
                    sa.Column('id', sa.String(), nullable=False),
                    sa.Column('created_at', sa.DateTime(), nullable=False),
                    sa.Column('updated_at', sa.DateTime(), nullable=False),
                    sa.Column('title', sa.String(), nullable=False),
                    sa.Column('description', sa.String(), nullable=False),
                    sa.ForeignKeyConstraint(['submenu_id'], ['submenu.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('dish')
    # ### end Alembic commands ###
