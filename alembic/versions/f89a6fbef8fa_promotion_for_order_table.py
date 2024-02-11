"""promotion_for_order table

Revision ID: f89a6fbef8fa
Revises: d0390f5f1465
Create Date: 2024-02-02 17:08:57.205790

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision: str = 'f89a6fbef8fa'
down_revision: Union[str, None] = 'd0390f5f1465'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'promotion_for_order',
        sa.Column('id', UUID(), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column('promotion_id', UUID(), nullable=False),
        sa.Column('purchase_order_id', UUID(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['promotion_id'], ['promotions.id'], onupdate='CASCADE', ondelete='RESTRICT'),
        sa.ForeignKeyConstraint(['purchase_order_id'], ['purchase_orders.id'], onupdate='CASCADE', ondelete='RESTRICT'),
        postgresql_tablespace='pg_default'
    )



def downgrade() -> None:
    op.drop_table('promotion_for_order')
