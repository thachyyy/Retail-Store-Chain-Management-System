"""create branch column in OrderDetail

Revision ID: 09054898e2d2
Revises: 84d78c7db7ca
Create Date: 2024-04-20 17:06:22.203849

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '09054898e2d2'
down_revision: Union[str, None] = '84d78c7db7ca'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('order', sa.Column('branch', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('order', 'branch')
    # ### end Alembic commands ###