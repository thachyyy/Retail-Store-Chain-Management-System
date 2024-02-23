"""employees table

Revision ID: a82ce9062958
Revises: 0f4efc4aab2f
Create Date: 2024-02-02 16:47:33.124567

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision: str = 'a82ce9062958'
down_revision: Union[str, None] = '0f4efc4aab2f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'employees',
        sa.Column('id', UUID(), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column('full_name', sa.String(), nullable=False),
        sa.Column('dob', sa.Date(), nullable=True),
        sa.Column('gender', sa.String(), nullable=True),
        sa.Column('email', sa.String(), nullable=True),
        sa.Column('phone_number', sa.String(), nullable=False),
        sa.Column('role', sa.String(), nullable=False),
        sa.Column('address', sa.String(), nullable=False),
        sa.Column('district', sa.String(), nullable=True),
        sa.Column('province', sa.String(), nullable=True),
        sa.Column('status', sa.String(), nullable=False),
        sa.Column('note', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email', name='employees_email_key'),
        sa.UniqueConstraint('phone_number', name='employees_phone_number_key'),
        postgresql_tablespace='pg_default'
    )


def downgrade() -> None:
    op.drop_table('employees')
