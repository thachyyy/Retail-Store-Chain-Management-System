import logging

from typing import Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.depends import oauth2
from app.api.depends.oauth2 import create_access_token, create_refresh_token, verify_refresh_token
from app.constant.app_status import AppStatus
from app.core.exceptions import error_exception_handler
from app.db.database import get_db
from app.models import Customer
from app.schemas import ChangePassword, CustomerResponse
from app.schemas.customer import CustomerCreateParams
from app.services.customer import CustomerService
from app.utils.response import make_response_object

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/customers")
async def create_customer(
    customer_create: CustomerCreateParams,
    db: Session = Depends(get_db)
) -> Any:
    customer_service = CustomerService(db=db)
    logger.info("Endpoints: create_customer called.")
    
    customer_response = await customer_service.create_customer(customer_create)
    logger.info("Endpoints: create_customer called successfully.")
    return make_response_object(customer_response)

@router.get("/customers")
async def   get_all_customers(db: Session = Depends(get_db)) -> Any:
    customer_service = CustomerService(db=db)
    logger.info("Endpoints: get_all_customers called.")
    
    customer_response = await customer_service.get_all_customers()
    logger.info("Endpoints: get_all_customers called successfully.")
    return make_response_object(customer_response)