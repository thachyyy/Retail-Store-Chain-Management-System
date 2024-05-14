"""update table

Revision ID: bdfdfdbf133e
Revises: 6e5a7258874b
Create Date: 2024-05-11 22:27:25.493577

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'bdfdfdbf133e'
down_revision: Union[str, None] = '6e5a7258874b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('inventory_check',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text("timezone('Asia/Ho_Chi_Minh', now())"), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('tenant_id', sa.String(), nullable=True),
    sa.Column('branch_id', sa.String(), nullable=True),
    sa.Column('product_id', sa.String(), nullable=True),
    sa.Column('batch_id', sa.String(), nullable=True),
    sa.Column('real_quantity', sa.Integer(), nullable=True),
    sa.Column('quantiry_in_db', sa.Integer(), nullable=True),
    sa.Column('difference', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_inventorycheck'))
    )
    op.drop_table('inventory_check')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('inventory_check',
    sa.Column('created_at', postgresql.TIMESTAMP(), server_default=sa.text("timezone('Asia/Ho_Chi_Minh'::text, now())"), autoincrement=False, nullable=True),
    sa.Column('updated_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('tenant_id', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('branch_id', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('product_id', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('batch_id', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('real_quantity', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('quantiry_in_db', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('difference', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=False)
    )
    op.drop_table('inventorycheck')
    # ### end Alembic commands ###