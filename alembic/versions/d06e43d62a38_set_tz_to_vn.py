"""Set TZ to VN.

Revision ID: d06e43d62a38
Revises: e335f4971988
Create Date: 2024-04-10 20:48:20.586678

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd06e43d62a38'
down_revision: Union[str, None] = 'e335f4971988'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('purchase_order', sa.Column('created_at', sa.DateTime(), server_default=sa.text("timezone('Asia/Ho_Chi_Minh', now())"), nullable=True))
    op.add_column('purchase_order', sa.Column('updated_at', sa.DateTime(), nullable=True))
    op.add_column('vendor', sa.Column('created_at', sa.DateTime(), server_default=sa.text("timezone('Asia/Ho_Chi_Minh', now())"), nullable=True))
    op.add_column('vendor', sa.Column('updated_at', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('vendor', 'updated_at')
    op.drop_column('vendor', 'created_at')
    op.drop_column('purchase_order', 'updated_at')
    op.drop_column('purchase_order', 'created_at')
    # ### end Alembic commands ###