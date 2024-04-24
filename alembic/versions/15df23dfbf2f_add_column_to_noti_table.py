"""add column to noti table

Revision ID: 15df23dfbf2f
Revises: 0b81e49039a7
Create Date: 2024-04-22 22:04:53.864805

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '15df23dfbf2f'
down_revision: Union[str, None] = '0b81e49039a7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('noti', sa.Column('tenant_id', sa.String(), nullable=False))
    op.add_column('noti', sa.Column('branch', sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('noti', 'branch')
    op.drop_column('noti', 'tenant_id')
    # ### end Alembic commands ###