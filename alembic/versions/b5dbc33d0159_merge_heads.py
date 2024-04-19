"""merge heads

Revision ID: b5dbc33d0159
Revises: a5f2581af324, 47e492211d04
Create Date: 2024-04-19 16:18:20.224342

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b5dbc33d0159'
down_revision: Union[str, None] = ('a5f2581af324', '47e492211d04')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
