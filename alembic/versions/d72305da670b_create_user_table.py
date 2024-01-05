"""create user table

Revision ID: d72305da670b
Revises: 0d249a9f2736
Create Date: 2023-10-29 16:25:01.619456

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd72305da670b'
down_revision = '0d249a9f2736'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('user',
                    sa.Column('id', sa.String(length=255), nullable=False),
                    sa.Column('authenticated_google_id', sa.String(length=255), nullable=True),
                    sa.Column('authenticated_apple', sa.String(length=255), nullable=True),
                    sa.Column('username', sa.String(length=40), nullable=False),
                    sa.Column('email', sa.String(length=255), nullable=False),
                    sa.Column('hashed_password', sa.String(), nullable=True),
                    sa.Column('first_name', sa.String(length=255), nullable=True),
                    sa.Column('last_name', sa.String(length=255), nullable=True),
                    sa.Column('phone', sa.String(length=255), nullable=True),
                    sa.Column('profile_image', sa.String(), nullable=True),
                    sa.Column('is_register', sa.Boolean(), server_default=sa.text('false'), nullable=False),
                    sa.Column('verify_code', sa.VARCHAR(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )


def downgrade() -> None:
    op.drop_table('user')
