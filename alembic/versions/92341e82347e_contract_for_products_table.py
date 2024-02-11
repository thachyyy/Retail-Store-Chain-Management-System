"""contract_for_products table

Revision ID: 92341e82347e
Revises: fbd35a81e8ea
Create Date: 2024-02-02 17:02:36.382687

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision: str = '92341e82347e'
down_revision: Union[str, None] = 'fbd35a81e8ea'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'contract_for_product',
        sa.Column('id', UUID(), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column('contract_id', UUID(), nullable=False),
        sa.Column('product_id', UUID(), nullable=False),
        sa.Column('price', sa.Float(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['contract_id'], ['contracts.id'], onupdate='CASCADE', ondelete='RESTRICT'),
        sa.ForeignKeyConstraint(['product_id'], ['products.id'], onupdate='CASCADE', ondelete='RESTRICT'),
        postgresql_tablespace='pg_default'
    )


def downgrade() -> None:
    op.drop_table('contract_for_product')
