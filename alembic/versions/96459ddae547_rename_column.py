"""rename column

Revision ID: 96459ddae547
Revises: 09054898e2d2
Create Date: 2024-04-20 22:07:29.419752

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '96459ddae547'
down_revision: Union[str, None] = '09054898e2d2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Đổi tên cột 'old_column_name' trong bảng 'table_name' thành 'new_column_name'
    op.alter_column('batch', 'belong_to_branch',new_column_name='branch')
def downgrade():
    # Trong trường hợp muốn rollback, đổi lại tên cột từ 'new_column_name' thành 'old_column_name'
    pass