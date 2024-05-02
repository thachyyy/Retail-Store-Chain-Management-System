"""drop column to contract

Revision ID: 5bf74c2396f8
Revises: 6da8843d5a2a
Create Date: 2024-05-02 15:22:08.596676

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5bf74c2396f8'
down_revision: Union[str, None] = '6da8843d5a2a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('contract_for_vendor', 'period')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('contract_for_vendor', sa.Column('period', sa.VARCHAR(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###