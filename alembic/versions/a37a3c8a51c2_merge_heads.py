"""merge heads

Revision ID: a37a3c8a51c2
Revises: 5719c2c39124, d12ecc990e97
Create Date: 2024-03-14 18:35:28.544231

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a37a3c8a51c2'
down_revision: Union[str, None] = ('5719c2c39124', 'd12ecc990e97')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
