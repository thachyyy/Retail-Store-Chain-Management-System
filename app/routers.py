from fastapi import APIRouter

# from app.api.endpoints import user
from app.api.endpoints import customer
from app.api.endpoints import vendor



router = APIRouter()

# router.include_router(user.router, prefix="", tags=["users"])
router.include_router(customer.router, prefix="", tags=["customers"])
router.include_router(vendor.router, prefix="", tags=["vendors"])


