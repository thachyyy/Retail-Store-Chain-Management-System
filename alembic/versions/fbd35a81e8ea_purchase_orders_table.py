"""purchase_orders table

Revision ID: fbd35a81e8ea
Revises: 3bd1ae911b65
Create Date: 2024-02-02 17:01:22.669903

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision: str = 'fbd35a81e8ea'
down_revision: Union[str, None] = '3bd1ae911b65'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'purchase_orders',
        sa.Column('id', UUID(), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False),
        sa.Column('estimated_delivery_date', sa.TIMESTAMP(), nullable=True),
        sa.Column('tax', sa.Float(), nullable=True),
        sa.Column('subtotal', sa.Float(), nullable=False),
        sa.Column('promote', sa.Float(), nullable=True),
        sa.Column('total', sa.Float(), nullable=False),
        sa.Column('tax_percentage', sa.Float(), nullable=False),
        sa.Column('status', sa.String(), nullable=True),
        sa.Column('note', sa.Text(), nullable=True),
        sa.Column('handled_by', UUID(), nullable=False),
        sa.Column('belong_to_cus', UUID(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['belong_to_cus'], ['customers.id'], onupdate='CASCADE', ondelete='RESTRICT'),
        sa.ForeignKeyConstraint(['handled_by'], ['employees.id'], onupdate='CASCADE', ondelete='RESTRICT'),
        postgresql_tablespace='pg_default'
    )


def downgrade() -> None:
    op.drop_table('purchase_orders')
