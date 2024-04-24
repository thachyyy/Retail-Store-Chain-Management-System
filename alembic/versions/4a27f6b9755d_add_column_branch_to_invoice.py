"""add column branch to invoice

Revision ID: 4a27f6b9755d
Revises: f61cf3a976fa
Create Date: 2024-04-20 11:14:42.618127

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4a27f6b9755d'
down_revision: Union[str, None] = 'f61cf3a976fa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('invoice_for_customer', sa.Column('branch', sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('invoice_for_customer', 'branch')
    # ### end Alembic commands ###