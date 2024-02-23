"""invoice_from_vendors table

Revision ID: 7fd7be56c9d6
Revises: 46fbe9a1ac80
Create Date: 2024-02-02 16:54:48.957554

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision: str = '7fd7be56c9d6'
down_revision: Union[str, None] = '46fbe9a1ac80'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'invoice_from_vendors',
        sa.Column('id', UUID(), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False),
        sa.Column('payment_deadline', sa.Date(), nullable=False),
        sa.Column('total', sa.Float(), nullable=False),
        sa.Column('status', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        postgresql_tablespace='pg_default'
    )


def downgrade() -> None:
    op.drop_table('invoice_from_vendors')
