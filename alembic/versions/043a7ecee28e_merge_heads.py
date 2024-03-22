"""merge heads

Revision ID: 043a7ecee28e
Revises: f49c6eb2f23e, feb9dc973ba3
Create Date: 2024-03-22 18:09:38.237309

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '043a7ecee28e'
down_revision: Union[str, None] = ('f49c6eb2f23e', 'feb9dc973ba3')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
