"""Update constrain field vendor.

Revision ID: 6920a16ffabb
Revises: fc21d6979993
Create Date: 2024-04-03 16:36:07.696746

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6920a16ffabb'
down_revision: Union[str, None] = 'fc21d6979993'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('vendor', 'phone_number',
               existing_type=sa.VARCHAR(length=255),
               nullable=True)
    op.alter_column('vendor', 'email',
               existing_type=sa.VARCHAR(length=255),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('vendor', 'email',
               existing_type=sa.VARCHAR(length=255),
               nullable=False)
    op.alter_column('vendor', 'phone_number',
               existing_type=sa.VARCHAR(length=255),
               nullable=False)
    # ### end Alembic commands ###
