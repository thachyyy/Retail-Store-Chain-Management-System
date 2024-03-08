"""Create tables cont.

Revision ID: 71c6f9178ade
Revises: 9a46e1bf26bc
Create Date: 2024-03-08 17:14:23.999901

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '71c6f9178ade'
down_revision: Union[str, None] = '9a46e1bf26bc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key('fk_contract_vendor', 'contract', 'vendor', ['belong_to_vendor'], ['vendor_name'])
    op.create_foreign_key('fk_contract_for_product_product', 'contract_for_product', 'product', ['product_id'], ['id'])
    op.create_foreign_key('fk_contract_for_product_contract', 'contract_for_product', 'contract', ['contract_id'], ['id'])
    op.create_foreign_key('fk_employee_branch', 'employee', 'branch', ['branch_name'], ['name_detail'])
    op.create_foreign_key('fk_invoice_for_customer_purchase_order', 'invoice_for_customer', 'purchase_order', ['belong_to_order'], ['id'])
    op.create_foreign_key('fk_order_of_batch_batch', 'order_of_batch', 'batch', ['batch_id'], ['id'])
    op.create_foreign_key('fk_order_of_batch_purchase_order', 'order_of_batch', 'purchase_order', ['purchase_order_id'], ['id'])
    op.create_foreign_key('fk_product_promotion', 'product', 'promotion', ['promotion_id'], ['id'])
    op.create_foreign_key('fk_product_contract', 'product', 'contract', ['contract_id'], ['id'])
    op.create_foreign_key('fk_product_batch', 'product', 'batch', ['batch_id'], ['id'])
    op.add_column('promotion', sa.Column('vendor_id', postgresql.UUID(), nullable=False))
    op.create_foreign_key('fk_promotion_vendor', 'promotion', 'vendor', ['vendor_id'], ['id'])
    op.create_foreign_key('fk_promotion_for_order_purchase_order', 'promotion_for_order', 'purchase_order', ['purchase_order_id'], ['id'])
    op.create_foreign_key('fk_promotion_for_order_promotion', 'promotion_for_order', 'promotion', ['promotion_id'], ['id'])
    op.create_foreign_key('fk_purchase_order_employee', 'purchase_order', 'employee', ['handle_by'], ['id'])
    op.create_foreign_key('fk_purchase_order_customer', 'purchase_order', 'customer', ['belong_to_customer'], ['id'])
    op.create_unique_constraint('unique_system_settings_id', 'system_settings', ['id'])
    op.create_foreign_key('fk_warehouse_receipt_employee', 'warehouse_receipt', 'employee', ['created_by'], ['id'])
    op.create_foreign_key('fk_warehouse_receipt_invoice_from_vendor', 'warehouse_receipt', 'invoice_from_vendor', ['belong_to_invoice'], ['id'])
    op.create_foreign_key('fk_warehouse_receipt_contract', 'warehouse_receipt', 'contract', ['belong_to_contract'], ['id'])
    op.create_foreign_key('fk_warehouse_receipt_vendor', 'warehouse_receipt', 'vendor', ['belong_to_vendor'], ['id'])
    # ### end Alembic commands ###
def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('fk_warehouse_receipt_vendor', 'warehouse_receipt', type_='foreignkey')
    op.drop_constraint('fk_warehouse_receipt_contract', 'warehouse_receipt', type_='foreignkey')
    op.drop_constraint('fk_warehouse_receipt_invoice_from_vendor', 'warehouse_receipt', type_='foreignkey')
    op.drop_constraint('fk_warehouse_receipt_employee', 'warehouse_receipt', type_='foreignkey')
    op.drop_constraint('unique_system_settings_id', 'system_settings', type_='unique')
    op.drop_constraint('fk_purchase_order_customer', 'purchase_order', type_='foreignkey')
    op.drop_constraint('fk_purchase_order_employee', 'purchase_order', type_='foreignkey')
    op.drop_constraint('fk_promotion_for_order_promotion', 'promotion_for_order', type_='foreignkey')
    op.drop_constraint('fk_promotion_for_order_purchase_order', 'promotion_for_order', type_='foreignkey')
    op.drop_constraint('fk_promotion_vendor', 'promotion', type_='foreignkey')
    op.drop_column('promotion', 'vendor_id')
    op.drop_constraint('fk_product_batch', 'product', type_='foreignkey')
    op.drop_constraint('fk_product_contract', 'product', type_='foreignkey')
    op.drop_constraint('fk_product_promotion', 'product', type_='foreignkey')
    op.drop_constraint('fk_order_of_batch_purchase_order', 'order_of_batch', type_='foreignkey')
    op.drop_constraint('fk_order_of_batch_batch', 'order_of_batch', type_='foreignkey')
    op.drop_constraint('fk_invoice_for_customer_purchase_order', 'invoice_for_customer', type_='foreignkey')
    op.drop_constraint('fk_employee_branch', 'employee', type_='foreignkey')
    op.drop_constraint('fk_contract_for_product_contract', 'contract_for_product', type_='foreignkey')
    op.drop_constraint('fk_contract_for_product_product', 'contract_for_product', type_='foreignkey')
    op.drop_constraint('fk_contract_vendor', 'contract', type_='foreignkey')
    # ### end Alembic commands ###
