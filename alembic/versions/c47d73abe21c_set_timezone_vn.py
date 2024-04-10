"""Set timezone VN.

Revision ID: c47d73abe21c
Revises: ab7a6173076c
Create Date: 2024-04-10 18:50:44.191446

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c47d73abe21c'
down_revision: Union[str, None] = 'ab7a6173076c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('branch', sa.Column('created_at', sa.DateTime(), server_default=sa.text("timezone('Asia/Ho_Chi_Minh', now())"), nullable=True))
    op.add_column('branch', sa.Column('updated_at', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('branch', 'updated_at')
    op.drop_column('branch', 'created_at')
    # ### end Alembic commands ###
