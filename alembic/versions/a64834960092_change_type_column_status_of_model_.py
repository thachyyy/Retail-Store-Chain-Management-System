"""Change type column status of model branch

Revision ID: a64834960092
Revises: bc5ca38ccc28
Create Date: 2024-02-29 12:02:52.232733

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a64834960092'
down_revision: Union[str, None] = 'bc5ca38ccc28'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('branch', 'status',
               existing_type=sa.VARCHAR(length=255),
               type_=sa.String(length=16),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('branch', 'status',
               existing_type=sa.String(length=16),
               type_=sa.VARCHAR(length=255),
               nullable=True)
    # ### end Alembic commands ###
