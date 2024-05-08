"""change type column in ContractForVendor

Revision ID: 6149fd44e900
Revises: 217e458f5e45
Create Date: 2024-05-08 10:39:46.739263

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6149fd44e900'
down_revision: Union[str, None] = '217e458f5e45'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('contract_for_vendor', 'latest_import',
               existing_type=sa.VARCHAR(),
               type_=sa.Date(),
               existing_nullable=True)
    op.alter_column('contract_for_vendor', 'next_import',
               existing_type=sa.VARCHAR(),
               type_=sa.Date(),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('contract_for_vendor', 'next_import',
               existing_type=sa.Date(),
               type_=sa.VARCHAR(),
               existing_nullable=True)
    op.alter_column('contract_for_vendor', 'latest_import',
               existing_type=sa.Date(),
               type_=sa.VARCHAR(),
               existing_nullable=True)
    # ### end Alembic commands ###
