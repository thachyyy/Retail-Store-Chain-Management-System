"""system_settings table

Revision ID: 0897b1bee760
Revises: 
Create Date: 2024-02-02 12:57:21.996031

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision: str = '0897b1bee760'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('system_settings',
                    sa.Column('id', UUID(), server_default=sa.text('uuid_generate_v4()'), nullable=False),
                    sa.Column('is_maintain', sa.Boolean(), nullable=False, server_default=sa.text('false')),
                    sa.PrimaryKeyConstraint('id')
                    )


def downgrade() -> None:
    op.drop_table('system_settings')
