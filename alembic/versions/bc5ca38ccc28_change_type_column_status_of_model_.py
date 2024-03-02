"""Change type column status of model promotion. Remove column vendor_id

Revision ID: bc5ca38ccc28
Revises: 398725172196
Create Date: 2024-02-29 08:45:23.216656

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'bc5ca38ccc28'
down_revision: Union[str, None] = '398725172196'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('promotion', 'status',
               existing_type=postgresql.ENUM('ACTIVE', 'INACTIVE', 'PENDING', 'EMPTY', name='status'),
               type_=sa.String(length=16),
               existing_nullable=False)
    op.drop_constraint('promotion_vendor_id_fkey', 'promotion', type_='foreignkey')
    op.drop_column('promotion', 'vendor_id')
    op.create_unique_constraint(None, 'system_settings', ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'system_settings', type_='unique')
    op.add_column('promotion', sa.Column('vendor_id', postgresql.UUID(), autoincrement=False, nullable=False))
    op.create_foreign_key('promotion_vendor_id_fkey', 'promotion', 'vendor', ['vendor_id'], ['id'])
    op.alter_column('promotion', 'status',
               existing_type=sa.String(length=16),
               type_=postgresql.ENUM('ACTIVE', 'INACTIVE', 'PENDING', 'EMPTY', name='status'),
               existing_nullable=False)
    # ### end Alembic commands ###
