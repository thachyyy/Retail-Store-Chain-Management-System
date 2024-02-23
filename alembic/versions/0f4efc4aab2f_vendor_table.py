"""vendor table

Revision ID: 0f4efc4aab2f
Revises: 0897b1bee760
Create Date: 2024-02-02 16:37:08.511771

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision: str = '0f4efc4aab2f'
down_revision: Union[str, None] = '0897b1bee760'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'vendors',
        sa.Column('id', UUID(), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column('company_name', sa.String(), nullable=True),
        sa.Column('vendor_name', sa.String(), nullable=False),
        sa.Column('phone_number', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('address', sa.String(), nullable=False),
        sa.Column('district', sa.String(), nullable=True),
        sa.Column('province', sa.String(), nullable=True),
        sa.Column('status', sa.String(), nullable=True),
        sa.Column('note', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        postgresql_tablespace='pg_default'
    )


def downgrade() -> None:
    op.drop_table('vendors')
