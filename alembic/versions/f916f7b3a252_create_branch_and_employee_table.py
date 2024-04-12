"""Create branch_and_employee table

Revision ID: f916f7b3a252
Revises: d301f965d5e8
Create Date: 2024-04-12 19:35:44.418421

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f916f7b3a252'
down_revision: Union[str, None] = 'd301f965d5e8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('branch_employees',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('branch_id', sa.String(), nullable=True),
    sa.Column('employee_id', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['branch_id'], ['branch.id'], name=op.f('fk_branch_employees_branch_id_branch')),
    sa.ForeignKeyConstraint(['employee_id'], ['employee.id'], name=op.f('fk_branch_employees_employee_id_employee')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_branch_employees'))
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('branch_employees')
    # ### end Alembic commands ###