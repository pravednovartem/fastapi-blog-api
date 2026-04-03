"""create initial tables

Revision ID: 9485d0a17bb1
Revises: 94e25a28a3d4
Create Date: 2026-04-03 13:27:19.700671

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9485d0a17bb1'
down_revision: Union[str, Sequence[str], None] = '94e25a28a3d4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
