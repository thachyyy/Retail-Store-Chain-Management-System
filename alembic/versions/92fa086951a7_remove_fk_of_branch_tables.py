"""Remove FK of branch tables

Revision ID: 92fa086951a7
Revises: d4662e5ce4e5
Create Date: 2024-02-29 20:15:21.756560

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '92fa086951a7'
down_revision: Union[str, None] = 'd4662e5ce4e5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('branch_manager_id_fkey', 'branch', type_='foreignkey')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key('branch_manager_id_fkey', 'branch', 'employee', ['manager_id'], ['id'])
    # ### end Alembic commands ###
