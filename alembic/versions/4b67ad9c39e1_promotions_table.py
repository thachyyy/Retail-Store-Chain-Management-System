"""promotions table

Revision ID: 4b67ad9c39e1
Revises: a82ce9062958
Create Date: 2024-02-02 16:48:33.850629

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision: str = '4b67ad9c39e1'
down_revision: Union[str, None] = 'a82ce9062958'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'promotions',
        sa.Column('id', UUID(), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('type', sa.String(), nullable=False),
        sa.Column('start_date', sa.TIMESTAMP(), nullable=False),
        sa.Column('end_date', sa.TIMESTAMP(), nullable=False),
        sa.Column('discount_value', sa.Float(), nullable=True),
        sa.Column('discount_max_value', sa.Float(), nullable=True),
        sa.Column('min_prod_for_discount', sa.BigInteger(), nullable=True),
        sa.Column('discount_percentage', sa.Float(), nullable=True),
        sa.Column('min_order_val_for_discount', sa.Float(), nullable=True),
        sa.Column('status', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        postgresql_tablespace='pg_default'
    )


def downgrade() -> None:
    op.drop_table('promotions')
