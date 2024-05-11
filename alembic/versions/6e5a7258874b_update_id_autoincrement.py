"""update id autoincrement

Revision ID: 6e5a7258874b
Revises: 92e2f16be9c8
Create Date: 2024-05-11 22:12:57.196731

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6e5a7258874b'
down_revision: Union[str, None] = '92e2f16be9c8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('inventory_check', sa.Column('id', sa.Integer(), autoincrement=True, nullable=False))
    op.drop_column('inventory_check', 'id_')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('inventory_check', sa.Column('id_', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_column('inventory_check', 'id')
    # ### end Alembic commands ###
