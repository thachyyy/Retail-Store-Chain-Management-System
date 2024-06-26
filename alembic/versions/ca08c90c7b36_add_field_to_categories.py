"""Add field to categories.

Revision ID: ca08c90c7b36
Revises: feb9dc973ba3
Create Date: 2024-03-21 23:39:28.165949

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ca08c90c7b36'
down_revision: Union[str, None] = 'feb9dc973ba3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('categories', sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True))
    op.add_column('categories', sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('categories', 'updated_at')
    op.drop_column('categories', 'created_at')
    # ### end Alembic commands ###
