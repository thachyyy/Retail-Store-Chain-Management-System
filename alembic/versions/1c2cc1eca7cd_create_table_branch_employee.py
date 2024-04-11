"""Create table branch_employee.

Revision ID: 1c2cc1eca7cd
Revises: 66fc6512c48c
Create Date: 2024-04-10 16:19:12.356919

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1c2cc1eca7cd'
down_revision: Union[str, None] = '66fc6512c48c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('branch_employees',
    sa.Column('branch_id', sa.String(), nullable=False),
    sa.Column('employee_id', sa.String(), nullable=False),
    sa.Column('role', sa.String(length=25), nullable=False),
    sa.ForeignKeyConstraint(['branch_id'], ['branch.id'], name=op.f('fk_branch_employees_branch_id_branch')),
    sa.ForeignKeyConstraint(['employee_id'], ['employee.id'], name=op.f('fk_branch_employees_employee_id_employee')),
    sa.PrimaryKeyConstraint('branch_id', 'employee_id', name=op.f('pk_branch_employees'))
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('branch_employees')
    # ### end Alembic commands ###