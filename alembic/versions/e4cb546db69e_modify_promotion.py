"""modify promotion

Revision ID: e4cb546db69e
Revises: af1c3d99a374
Create Date: 2024-04-19 23:05:47.530283

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'e4cb546db69e'
down_revision: Union[str, None] = 'af1c3d99a374'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('import_order', 'belong_to_contract',
               existing_type=sa.VARCHAR(length=16),
               nullable=False)
    op.add_column('promotion', sa.Column('discount_percent', sa.Integer(), nullable=True))
    op.add_column('promotion', sa.Column('discount_value_max', sa.Integer(), nullable=True))
    op.add_column('promotion', sa.Column('min_total_valid', sa.Integer(), nullable=True))
    op.add_column('promotion', sa.Column('remaining_number', sa.Integer(), nullable=True))
    op.add_column('promotion', sa.Column('branch', sa.String(), nullable=True))
    op.alter_column('promotion', 'start_date',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('promotion', 'end_date',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.drop_constraint('fk_promotion_vendor', 'promotion', type_='foreignkey')
    op.drop_column('promotion', 'promotion_type')
    op.drop_column('promotion', 'min_product_value')
    op.drop_column('promotion', 'promotion_value')
    op.drop_column('promotion', 'max_discount_amount')
    op.drop_column('promotion', 'status')
    op.drop_column('promotion', 'vendor_id')
    op.drop_column('promotion', 'min_product_quantity')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('promotion', sa.Column('min_product_quantity', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('promotion', sa.Column('vendor_id', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.add_column('promotion', sa.Column('status', sa.VARCHAR(length=16), autoincrement=False, nullable=False))
    op.add_column('promotion', sa.Column('max_discount_amount', sa.INTEGER(), autoincrement=False, nullable=False))
    op.add_column('promotion', sa.Column('promotion_value', sa.INTEGER(), autoincrement=False, nullable=False))
    op.add_column('promotion', sa.Column('min_product_value', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('promotion', sa.Column('promotion_type', sa.VARCHAR(length=255), autoincrement=False, nullable=False))
    op.create_foreign_key('fk_promotion_vendor', 'promotion', 'vendor', ['vendor_id'], ['id'])
    op.alter_column('promotion', 'end_date',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('promotion', 'start_date',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.drop_column('promotion', 'branch')
    op.drop_column('promotion', 'remaining_number')
    op.drop_column('promotion', 'min_total_valid')
    op.drop_column('promotion', 'discount_value_max')
    op.drop_column('promotion', 'discount_percent')
    op.alter_column('import_order', 'belong_to_contract',
               existing_type=sa.VARCHAR(length=16),
               nullable=True)
    # ### end Alembic commands ###
