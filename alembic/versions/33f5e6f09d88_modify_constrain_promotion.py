"""modify constrain promotion

Revision ID: 33f5e6f09d88
Revises: e4cb546db69e
Create Date: 2024-04-19 23:14:53.892477

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '33f5e6f09d88'
down_revision: Union[str, None] = 'e4cb546db69e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('promotion', sa.Column('status', sa.String(), nullable=True))
    op.alter_column('promotion', 'branch',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('promotion', 'branch',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.drop_column('promotion', 'status')
    # ### end Alembic commands ###
