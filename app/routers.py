from fastapi import APIRouter

# from app.api.endpoints import user
from app.api.endpoints import branch
from app.api.endpoints import categories
from app.api.endpoints import contract
from app.api.endpoints import customer
from app.api.endpoints import employee
from app.api.endpoints import promotion
from app.api.endpoints import vendor



router = APIRouter()

# router.include_router(user.router, prefix="", tags=["users"])
router.include_router(branch.router, prefix="", tags=["branches"])
router.include_router(categories.router, prefix="", tags=["categories"])
router.include_router(contract.router, prefix="", tags=["contracts"])
router.include_router(customer.router, prefix="", tags=["customers"])
router.include_router(employee.router, prefix="", tags=["employees"])
router.include_router(promotion.router, prefix="", tags=["promotions"])
router.include_router(vendor.router, prefix="", tags=["vendors"])


