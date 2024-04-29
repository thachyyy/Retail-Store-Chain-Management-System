from fastapi import APIRouter

# from app.api.endpoints import user
from app.api.endpoints import branch
from app.api.endpoints import categories
from app.api.endpoints import contract_for_vendor
from app.api.endpoints import contract_for_product
from app.api.endpoints import customer

from app.api.endpoints import product
from app.api.endpoints import employee
from app.api.endpoints import promotion
from app.api.endpoints import vendor
from app.api.endpoints import invoice_for_customer
from app.api.endpoints import invoice_from_vendor
from app.api.endpoints import import_order
from app.api.endpoints import batch
from app.api.endpoints import order_of_batch
from app.api.endpoints import product_of_import_order
from app.api.endpoints import promotion_belong_to_branch
from app.api.endpoints import promotion_for_order
from app.api.endpoints import purchase_order
from app.api.endpoints import order_detail
from app.api.endpoints import import_detail
from app.api.endpoints import dashboard
from app.api.endpoints import noti
from app.api.endpoints import report
from app.api.endpoints import inventory_check


router = APIRouter()

# router.include_router(user.router, prefix="", tags=["users"])
router.include_router(dashboard.router, prefix="", tags=["dashboard"])
router.include_router(product.router, prefix="", tags=["products"])
router.include_router(categories.router, prefix="", tags=["categories"])
router.include_router(batch.router, prefix="", tags=["batch"])
router.include_router(purchase_order.router, prefix="", tags=["purchase_order"])
router.include_router(order_detail.router, prefix="", tags=["order_detail"])
router.include_router(customer.router, prefix="", tags=["customers"])
router.include_router(employee.router, prefix="", tags=["employees"])
router.include_router(branch.router, prefix="", tags=["branches"])
router.include_router(import_order.router, prefix="", tags=["import_order"])
router.include_router(import_detail.router, prefix="", tags=["import_detail"])
router.include_router(contract_for_product.router, prefix="", tags=["contract_for_product"])
router.include_router(contract_for_vendor.router, prefix="", tags=["contracts_for_vendor"])
router.include_router(invoice_for_customer.router, prefix="", tags=["invoice_for_customer"])
router.include_router(invoice_from_vendor.router, prefix="", tags=["invoice_from_vendor"])
router.include_router(noti.router, prefix="", tags=["noti"])
router.include_router(order_of_batch.router, prefix="", tags=["order_of_batch"])
router.include_router(product_of_import_order.router, prefix="", tags=["product_of_import_order"])
router.include_router(promotion_for_order.router, prefix="", tags=["promotion_for_order"])
router.include_router(promotion_belong_to_branch.router, prefix="", tags=["promotion_belong_to_branch"])
router.include_router(promotion.router, prefix="", tags=["promotions"])
router.include_router(vendor.router, prefix="", tags=["vendors"])
router.include_router(report.router, prefix="", tags=["reports"])
router.include_router(inventory_check.router, prefix="", tags=["inventory_check"])

