"""promotion_belong_to_branch table

Revision ID: d0390f5f1465
Revises: 40d2bfbd9c9e
Create Date: 2024-02-02 17:07:15.142206

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision: str = 'd0390f5f1465'
down_revision: Union[str, None] = '40d2bfbd9c9e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'promotion_belong_to_branch',
        sa.Column('id', UUID(), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column('promotion_id', UUID(), nullable=False),
        sa.Column('branch_id', UUID(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['promotion_id'], ['promotions.id'], onupdate='CASCADE', ondelete='RESTRICT'),
        sa.ForeignKeyConstraint(['branch_id'], ['branches.id'], onupdate='CASCADE', ondelete='RESTRICT'),
        postgresql_tablespace='pg_default'
    )


def downgrade() -> None:
    op.drop_table('promotion_belong_to_branch')
