"""change order_detail type to Int

Revision ID: bd100a8effd4
Revises: b66796fe7867
Create Date: 2024-04-16 22:31:17.667975

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'bd100a8effd4'
down_revision: Union[str, None] = 'b66796fe7867'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('invoice_for_customer', 'order_detail',
               existing_type=postgresql.ARRAY(sa.VARCHAR()),
               type_=sa.ARRAY(sa.Integer()),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('invoice_for_customer', 'order_detail',
               existing_type=sa.ARRAY(sa.Integer()),
               type_=postgresql.ARRAY(sa.VARCHAR()),
               existing_nullable=False)
    # ### end Alembic commands ###
