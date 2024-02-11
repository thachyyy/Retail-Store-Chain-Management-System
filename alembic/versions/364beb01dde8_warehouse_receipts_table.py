"""warehouse_receipts table

Revision ID: 364beb01dde8
Revises: 7fd7be56c9d6
Create Date: 2024-02-02 16:57:31.378166

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision: str = '364beb01dde8'
down_revision: Union[str, None] = '7fd7be56c9d6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'warehouse_receipts',
        sa.Column('id', UUID(), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column('is_contract', sa.Boolean(), nullable=False),
        sa.Column('estimated_date', sa.Date(), nullable=False),
        sa.Column('delivery_status', sa.String(), nullable=False),
        sa.Column('payment_status', sa.String(), nullable=False),
        sa.Column('subtotal', sa.Float(), nullable=False),
        sa.Column('promotion', sa.Float(), nullable=True),
        sa.Column('total', sa.Float(), nullable=False),
        sa.Column('created_by', UUID(), nullable=False),
        sa.Column('belong_to_vendor', UUID(), nullable=False),
        sa.Column('belong_to_contract', UUID(), nullable=False),
        sa.Column('belong_to_invoice', UUID(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['belong_to_contract'], ['contracts.id'], onupdate='CASCADE', ondelete='RESTRICT'),
        sa.ForeignKeyConstraint(['belong_to_invoice'], ['invoice_from_vendors.id'], onupdate='CASCADE', ondelete='RESTRICT'),
        sa.ForeignKeyConstraint(['belong_to_vendor'], ['vendors.id'], onupdate='CASCADE', ondelete='RESTRICT'),
        sa.ForeignKeyConstraint(['created_by'], ['employees.id'], onupdate='CASCADE', ondelete='RESTRICT'),
        postgresql_tablespace='pg_default'
    )


def downgrade() -> None:
    op.drop_table('warehouse_receipts')
