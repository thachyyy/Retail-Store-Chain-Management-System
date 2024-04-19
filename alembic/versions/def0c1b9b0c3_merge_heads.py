"""merge heads

Revision ID: def0c1b9b0c3
Revises: 8a10ba0df0b0, bd100a8effd4
Create Date: 2024-04-19 10:45:29.959546

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'def0c1b9b0c3'
down_revision: Union[str, None] = ('8a10ba0df0b0', 'bd100a8effd4')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
