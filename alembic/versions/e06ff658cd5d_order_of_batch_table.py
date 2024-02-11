"""order_of_batch table

Revision ID: e06ff658cd5d
Revises: fa1a570b43cc
Create Date: 2024-02-02 17:04:36.720577

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision: str = 'e06ff658cd5d'
down_revision: Union[str, None] = 'fa1a570b43cc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'order_of_batch',
        sa.Column('id', UUID(), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column('purchase_order_id', UUID(), nullable=False),
        sa.Column('batch_id', UUID(), nullable=False),
        sa.Column('price', sa.Float(), nullable=False),
        sa.Column('quantity', sa.BigInteger(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['batch_id'], ['batches.id'], onupdate='CASCADE', ondelete='RESTRICT'),
        sa.ForeignKeyConstraint(['purchase_order_id'], ['purchase_orders.id'], onupdate='CASCADE', ondelete='RESTRICT'),
        postgresql_tablespace='pg_default'
    )


def downgrade() -> None:
    op.drop_table('order_of_batch')
