"""Modify field employee contrain.

Revision ID: 2f94580ddb6a
Revises: ce20be0e657c
Create Date: 2024-03-29 17:04:24.774020

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2f94580ddb6a'
down_revision: Union[str, None] = 'ce20be0e657c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('employee', 'address',
               existing_type=sa.VARCHAR(length=255),
               nullable=True)
    op.alter_column('employee', 'district',
               existing_type=sa.VARCHAR(length=255),
               nullable=True)
    op.alter_column('employee', 'province',
               existing_type=sa.VARCHAR(length=255),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('employee', 'province',
               existing_type=sa.VARCHAR(length=255),
               nullable=False)
    op.alter_column('employee', 'district',
               existing_type=sa.VARCHAR(length=255),
               nullable=False)
    op.alter_column('employee', 'address',
               existing_type=sa.VARCHAR(length=255),
               nullable=False)
    # ### end Alembic commands ###
