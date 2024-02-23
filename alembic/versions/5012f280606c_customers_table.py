"""customers table

Revision ID: 5012f280606c
Revises: 364beb01dde8
Create Date: 2024-02-02 16:58:17.374457

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision: str = '5012f280606c'
down_revision: Union[str, None] = '364beb01dde8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'customers',
        sa.Column('id', UUID(), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column('full_name', sa.String(), nullable=False),
        sa.Column('dob', sa.Date(), nullable=True),
        sa.Column('gender', sa.String(), nullable=True),
        sa.Column('email', sa.String(), nullable=True),
        sa.Column('phone_number', sa.String(), nullable=False),
        sa.Column('address', sa.String(), nullable=True),
        sa.Column('district', sa.String(), nullable=True),
        sa.Column('province', sa.String(), nullable=True),
        sa.Column('reward_point', sa.BigInteger(), nullable=True),
        sa.Column('note', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email', name='customers_email_key'),
        sa.UniqueConstraint('phone_number', name='customers_phone_number_key'),
        postgresql_tablespace='pg_default'
    )


def downgrade() -> None:
    op.drop_table('customers')
