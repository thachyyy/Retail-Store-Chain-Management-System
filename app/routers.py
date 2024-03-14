from fastapi import APIRouter

# from app.api.endpoints import user
from app.api.endpoints import branch
from app.api.endpoints import categories
from app.api.endpoints import contract_for_vendor
from app.api.endpoints import contract_for_procduct
from app.api.endpoints import customer

from app.api.endpoints import product
from app.api.endpoints import employee
from app.api.endpoints import promotion
from app.api.endpoints import vendor
from app.api.endpoints import invoice_for_customer



router = APIRouter()

# router.include_router(user.router, prefix="", tags=["users"])
router.include_router(branch.router, prefix="", tags=["branches"])
router.include_router(categories.router, prefix="", tags=["categories"])
router.include_router(contract_for_vendor.router, prefix="", tags=["contracts"])
router.include_router(contract_for_procduct.router, prefix="", tags=["contract_for_products"])
router.include_router(customer.router, prefix="", tags=["customers"])
router.include_router(product.router, prefix="", tags=["product"])
router.include_router(employee.router, prefix="", tags=["employees"])
router.include_router(promotion.router, prefix="", tags=["promotions"])
router.include_router(vendor.router, prefix="", tags=["vendors"])
router.include_router(invoice_for_customer.router, prefix="", tags=["invoice_for_customer"])
