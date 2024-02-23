"""batches table

Revision ID: fd0cf24aaf37
Revises: 5012f280606c
Create Date: 2024-02-02 16:59:16.927797

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision: str = 'fd0cf24aaf37'
down_revision: Union[str, None] = '5012f280606c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'batches',
        sa.Column('id', UUID(), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column('quantity', sa.BigInteger(), nullable=False),
        sa.Column('import_price', sa.Float(), nullable=False),
        sa.Column('manufacturing_date', sa.Date(), nullable=False),
        sa.Column('expiry_date', sa.Date(), nullable=False),
        sa.Column('belong_to_branch', UUID(), nullable=False),
        sa.Column('belong_to_receipt', UUID(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['belong_to_branch'], ['branches.id'], onupdate='CASCADE', ondelete='RESTRICT'),
        sa.ForeignKeyConstraint(['belong_to_receipt'], ['warehouse_receipts.id'], onupdate='CASCADE', ondelete='RESTRICT'),
        postgresql_tablespace='pg_default'
    )


def downgrade() -> None:
    op.drop_table('batches')
