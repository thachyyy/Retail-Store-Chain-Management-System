"""add column branch in employee.

Revision ID: 2ee386970d5d
Revises: 479cada4d3fb
Create Date: 2024-04-17 16:14:09.335914

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2ee386970d5d'
down_revision: Union[str, None] = '479cada4d3fb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('employee', sa.Column('branch', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('employee', 'branch')
    # ### end Alembic commands ###
