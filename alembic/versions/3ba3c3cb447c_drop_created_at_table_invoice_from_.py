"""Drop created_at table invoice_from_vendor.

Revision ID: 3ba3c3cb447c
Revises: 8baf3f8fffb1
Create Date: 2024-04-10 20:38:13.447618

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '3ba3c3cb447c'
down_revision: Union[str, None] = '8baf3f8fffb1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('invoice_from_vendor', 'created_at')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('invoice_from_vendor', sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
