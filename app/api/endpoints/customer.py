import logging

from typing import Any, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from pydantic import UUID4
from datetime import date

from app.api.depends import oauth2
# from app.api.depends.oauth2 import create_access_token, create_refresh_token, verify_refresh_token
from app.constant.app_status import AppStatus
from app.core.exceptions import error_exception_handler
from app.db.database import get_db
from app.models import Customer
# from app.schemas import ChangePassword, CustomerResponse
from app.schemas.customer import CustomerCreateParams, CustomerUpdate
from app.services.customer import CustomerService
from app.utils.response import make_response_object
from app.models import Employee

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/customers")
async def create_customer(
    customer_create: CustomerCreateParams,
    user: Employee = Depends(oauth2.get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    current_user = await user
    
    customer_service = CustomerService(db=db)
    logger.info("Endpoints: create_customer called.")
    
    msg, customer_response = await customer_service.create_customer(current_user.tenant_id, customer_create)
    logger.info("Endpoints: create_customer called successfully.")
    return make_response_object(customer_response, msg)

@router.get("/customers")
async def get_all_customers(
    db: Session = Depends(get_db),
    user: Employee = Depends(oauth2.get_current_user),
    limit: int = None,
    offset: int = None,
    gender: str = None,
    start_date: date = None,
    end_date: date = None,
    province: str = None,
    district: str = None,
    query_search: Optional[str] = None,
) -> Any:
    
    current_user = await user
    
    customer_service = CustomerService(db=db)
    logger.info("Endpoints: get_all_customers called.")
    
    msg, customer_response = await customer_service.get_all_customers(current_user.tenant_id, limit,offset, gender, start_date, end_date, province, district, query_search)
    logger.info("Endpoints: get_all_customers called successfully.")
    return make_response_object(customer_response, msg)

@router.get("/customers/{id}")
async def get_customer_by_id(
    id: str, 
    db: Session = Depends(get_db),
    user: Employee = Depends(oauth2.get_current_user),
) -> Any:
    
    current_user = await user
    
    customer_service = CustomerService(db=db)
    
    logger.info("Endpoints: get_customer_by_id called.")  
    msg, customer_response = await customer_service.get_customer_by_id(current_user.tenant_id, id)
    logger.info("Endpoints: get_all_customers called successfully.")
    return make_response_object(customer_response, msg)
    
@router.put("/customers/{customer_id}")
async def update_customer(
    customer_id: str, 
    customer_update: CustomerUpdate, 
    db: Session = Depends(get_db),
    user: Employee = Depends(oauth2.get_current_user),
) -> Any:
    
    current_user = await user
    
    customer_service = CustomerService(db=db)
    
    logger.info("Endpoints: update_customer called.")
    msg, customer_response = await customer_service.update_customer(current_user.tenant_id, customer_id, customer_update)
    logger.info("Endpoints: update_customer called successfully.")
    return make_response_object(customer_response, msg)

@router.delete("/customers/{customer_id}")
async def delete_customer(
    customer_id: str, 
    db: Session = Depends(get_db),
    user: Employee = Depends(oauth2.get_current_user),
) -> Any:
    
    current_user = await user
    
    customer_service = CustomerService(db=db)
    
    logger.info("Endpoints: delete_customer called.")
    msg, customer_response = await customer_service.delete_customer(current_user.tenant_id, customer_id)
    logger.info("Endpoints: delete_customer called successfully.")
    return make_response_object(customer_response, msg)

@router.get("/customer/search")
async def search_customer(
    db: Session = Depends(get_db), 
    condition: Optional[str] = Query(None),
    limit: Optional[int] = None,
    offset:Optional[int] = None
) -> Any:
    customer_service = CustomerService(db=db)
    
    logger.info("Endpoints: search_customer called.")
    msg, customer_response = await customer_service.search_customer(condition, limit, offset)
    logger.info("Endpoints: search_customer called successfully.")
    
    return make_response_object(customer_response, msg)

@router.get("/customers/filter")
async def filter_customer(
    db: Session = Depends(get_db),
    gender: str = None,
    start_date: date = None,
    end_date: date = None,
    province: str = None,
    district: str = None,
) -> Any:
    customer_service = CustomerService(db=db)
    
    logger.info("Endpoints: filter_customer called.")
    msg, customer_response = await customer_service.filter_customer(gender, start_date, end_date, province, district)
    logger.info("Endpoints: filter_customer called successfully.")
    
    return make_response_object(customer_response, msg)