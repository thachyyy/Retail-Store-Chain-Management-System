"""merge heads

Revision ID: ce20be0e657c
Revises: 585a13ea3e79, 043a7ecee28e
Create Date: 2024-03-23 11:05:04.606856

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ce20be0e657c'
down_revision: Union[str, None] = ('585a13ea3e79', '043a7ecee28e')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
