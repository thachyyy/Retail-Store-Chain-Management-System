"""contracts table

Revision ID: 46fbe9a1ac80
Revises: 96336847ea4a
Create Date: 2024-02-02 16:52:31.672320

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision: str = '46fbe9a1ac80'
down_revision: Union[str, None] = '96336847ea4a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'contracts',
        sa.Column('id', UUID(), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column('start_date', sa.TIMESTAMP(), nullable=False),
        sa.Column('end_date', sa.TIMESTAMP(), nullable=False),
        sa.Column('minimum_order_amount', sa.Float(), nullable=True),
        sa.Column('minimum_order_quantity', sa.BigInteger(), nullable=True),
        sa.Column('ordering_cycle_amount', sa.BigInteger(), nullable=True),
        sa.Column('ordering_cycle_quantity', sa.BigInteger(), nullable=True),
        sa.Column('belong_to_vendor', UUID(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['belong_to_vendor'], ['vendors.id'], onupdate='CASCADE', ondelete='RESTRICT'),
        postgresql_tablespace='pg_default'
    )


def downgrade() -> None:
    op.drop_table('contracts')
