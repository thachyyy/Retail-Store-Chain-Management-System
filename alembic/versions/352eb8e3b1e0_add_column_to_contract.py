"""add column to contract

Revision ID: 352eb8e3b1e0
Revises: 5bf74c2396f8
Create Date: 2024-05-02 15:22:41.721217

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '352eb8e3b1e0'
down_revision: Union[str, None] = '5bf74c2396f8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('contract_for_vendor', sa.Column('period', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('contract_for_vendor', 'period')
    # ### end Alembic commands ###
