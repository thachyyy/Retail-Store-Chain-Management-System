"""product_of_warehouse_receipt table

Revision ID: 40d2bfbd9c9e
Revises: e06ff658cd5d
Create Date: 2024-02-02 17:06:14.173097

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision: str = '40d2bfbd9c9e'
down_revision: Union[str, None] = 'e06ff658cd5d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'product_of_warehouse_receipt',
        sa.Column('id', UUID(), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column('product_id', UUID(), nullable=False),
        sa.Column('warehouse_receipt_id', UUID(), nullable=False),
        sa.Column('import_price', sa.Float(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['product_id'], ['products.id'], onupdate='CASCADE', ondelete='RESTRICT'),
        sa.ForeignKeyConstraint(['warehouse_receipt_id'], ['warehouse_receipts.id'], onupdate='CASCADE', ondelete='RESTRICT'),
        postgresql_tablespace='pg_default'
    )


def downgrade() -> None:
    op.drop_table('product_of_warehouse_receipt')
