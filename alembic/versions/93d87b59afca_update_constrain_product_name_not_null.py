"""Update constrain product_name not null.

Revision ID: 93d87b59afca
Revises: 6920a16ffabb
Create Date: 2024-04-09 22:30:01.215860

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '93d87b59afca'
down_revision: Union[str, None] = '6920a16ffabb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    # op.drop_index('ix_user_email', table_name='user')
    # op.drop_index('ix_user_username', table_name='user')
    # op.drop_table('user')
    op.alter_column('product', 'product_name',
               existing_type=sa.VARCHAR(length=255),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('product', 'product_name',
               existing_type=sa.VARCHAR(length=255),
               nullable=True)
    op.create_table('user',
    sa.Column('id', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('username', sa.VARCHAR(length=42), autoincrement=False, nullable=False),
    sa.Column('email', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('hashed_password', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('first_name', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('last_name', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('verify_code', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('phone', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('authenticated_google_id', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('authenticated_apple', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('is_register', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='pk_user')
    )
    op.create_index('ix_user_username', 'user', ['username'], unique=False)
    op.create_index('ix_user_email', 'user', ['email'], unique=False)
    # ### end Alembic commands ###