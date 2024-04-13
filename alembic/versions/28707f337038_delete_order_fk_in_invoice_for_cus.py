"""delete order fk in invoice for cus

Revision ID: 28707f337038
Revises: b5bff4cf8785
Create Date: 2024-04-13 10:25:31.637943

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '28707f337038'
down_revision: Union[str, None] = 'b5bff4cf8785'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('fk_invoice_for_customer_order_detail_order', 'invoice_for_customer', type_='foreignkey')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass    # ### end Alembic commands ###