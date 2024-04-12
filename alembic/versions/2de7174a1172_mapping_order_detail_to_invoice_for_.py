"""Mapping order_detail to invoice_for_customer

Revision ID: 2de7174a1172
Revises: f916f7b3a252
Create Date: 2024-04-12 22:44:11.463866

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2de7174a1172'
down_revision: Union[str, None] = 'f916f7b3a252'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('invoice_for_customer', sa.Column('order_detail', sa.Integer(), nullable=False))
    op.create_unique_constraint(op.f('uq_invoice_for_customer_order_detail'), 'invoice_for_customer', ['order_detail'])
    op.create_foreign_key(op.f('fk_invoice_for_customer_order_detail_order'), 'invoice_for_customer', 'order', ['order_detail'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass 
    # ### end Alembic commands ###