"""products table

Revision ID: 3bd1ae911b65
Revises: fd0cf24aaf37
Create Date: 2024-02-02 17:00:11.745415

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision: str = '3bd1ae911b65'
down_revision: Union[str, None] = 'fd0cf24aaf37'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'products',
        sa.Column('id', UUID(), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('brand', sa.String(), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('img_url', sa.String(), nullable=True),
        sa.Column('price', sa.Float(), nullable=True),
        sa.Column('status', sa.String(), nullable=True),
        sa.Column('belong_to_category', UUID(), nullable=True),
        sa.Column('belong_to_batch', UUID(), nullable=False),
        sa.Column('has_promotion', UUID(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['belong_to_batch'], ['batches.id'], onupdate='CASCADE', ondelete='RESTRICT'),
        sa.ForeignKeyConstraint(['belong_to_category'], ['categories.id'], onupdate='CASCADE', ondelete='RESTRICT'),
        sa.ForeignKeyConstraint(['has_promotion'], ['promotions.id'], onupdate='CASCADE', ondelete='RESTRICT'),
        postgresql_tablespace='pg_default'
    )


def downgrade() -> None:
    op.drop_table('products')
