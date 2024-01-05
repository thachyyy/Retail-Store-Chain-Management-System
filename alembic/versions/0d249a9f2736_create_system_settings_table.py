"""create_system_settings_table

Revision ID: 0d249a9f2736
Revises: 
Create Date: 2023-10-29 16:23:42.591131

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision = '0d249a9f2736'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('system_settings',
                    sa.Column('id', UUID(), server_default=sa.text('uuid_generate_v4()'), nullable=False),
                    sa.Column('is_maintain', sa.Boolean(), nullable=False, server_default=sa.text('false')),
                    sa.PrimaryKeyConstraint('id')
                    )


def downgrade():
    op.drop_table('system_settings')
