"""add user password and unique username.

Revision ID: b1c2a3d4e5f6
Revises: 94e25a28a3d4
Create Date: 2026-05-03 15:25:00.000000

"""
from typing import Sequence, Union

from alembic import op

import sqlalchemy as sa


revision: str = 'b1c2a3d4e5f6'
down_revision: Union[str, Sequence[str], None] = '94e25a28a3d4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Добавить колонку password и уникальный индекс на username."""
    with op.batch_alter_table('auth_user') as batch_op:
        batch_op.add_column(sa.Column('password', sa.String(), nullable=True))
        batch_op.create_unique_constraint(
            'uq_auth_user_username',
            ['username'],
        )


def downgrade() -> None:
    """Откатить изменения: убрать password и уникальность username."""
    with op.batch_alter_table('auth_user') as batch_op:
        batch_op.drop_constraint('uq_auth_user_username', type_='unique')
        batch_op.drop_column('password')
