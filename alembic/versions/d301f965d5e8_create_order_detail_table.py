"""Create order detail table

Revision ID: d301f965d5e8
Revises: aec69d02ff61
Create Date: 2024-04-12 14:34:53.072952

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd301f965d5e8'
down_revision: Union[str, None] = 'aec69d02ff61'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('order',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('batch_id', sa.String(), nullable=True),
    sa.Column('purchase_order_id', sa.String(), nullable=True),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.Column('price', sa.Integer(), nullable=True),
    sa.Column('sub_total', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['batch_id'], ['batch.id'], name=op.f('fk_order_batch_id_batch')),
    sa.ForeignKeyConstraint(['purchase_order_id'], ['purchase_order.id'], name=op.f('fk_order_purchase_order_id_purchase_order')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_order'))
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('order')
    # ### end Alembic commands ###
