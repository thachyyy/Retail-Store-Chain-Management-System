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
from app.models import InvoiceForCustomer
# from app.schemas import ChangePassword, InvoiceForCustomerResponse
from app.models.employee import Employee
from app.schemas.invoice_for_customer import InvoiceForCustomerCreateParams, InvoiceForCustomerUpdate
from app.services.invoice_for_customer import InvoiceForCustomerService
from app.utils.response import make_response_object

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/invoice_for_customers")
async def create_invoice_for_customer(
    paid:bool,
    invoice_for_customer_create: InvoiceForCustomerCreateParams,
    user: Employee = Depends(oauth2.get_current_user),
    branch_name: Optional[str] = None,
    db: Session = Depends(get_db)
) -> Any:
    current_user = await user
    
    if branch_name:
        branch = branch_name
    else:
        branch = current_user.branch
    
    invoice_for_customer_service = InvoiceForCustomerService(db=db)
    logger.info("Endpoints: create_invoice_for_customer called.")
    msg, invoice_for_customer_response = await invoice_for_customer_service.create_invoice_for_customer(paid,invoice_for_customer_create,current_user.tenant_id,branch)
    logger.info("Endpoints: create_invoice_for_customer called successfully.")
    return make_response_object(invoice_for_customer_response, msg)

@router.get("/invoice_for_customers")
async def get_all_invoice_for_customers(
    db: Session = Depends(get_db),
    user: Employee = Depends(oauth2.get_current_user),
    branch_name: Optional[str] = None,
    limit: Optional[int] = None,
    offset:Optional[int] = None,
    status:Optional[str] = None,
    gt_total:Optional[int] = None,
    lt_total:Optional[int] = None,
    start_date:Optional[date] = None,
    end_date:Optional[date] = None,
    query_search:Optional[str] = None
) -> Any:
    current_user = await user
    
    if branch_name:
        branch = branch_name
    else:
        branch = current_user.branch
        
    invoice_for_customer_service = InvoiceForCustomerService(db=db)
    logger.info("Endpoints: get_all_invoice_for_customers called.")
    
    msg, invoice_for_customer_response = await invoice_for_customer_service.get_all_invoice_for_customers(
        current_user.tenant_id,
        branch,
        limit=limit,
        offset=offset,
        status=status,
        gt_total=gt_total,
        lt_total=lt_total,
        start_date=start_date,
        end_date=end_date,
        query_search=query_search
    )
    logger.info("Endpoints: get_all_invoice_for_customers called successfully.")
    return make_response_object(invoice_for_customer_response, msg)

@router.get("/invoice_for_customers/{invoice_for_customer_id}")
async def get_invoice_for_customer_by_id(
    invoice_for_customer_id: str, 
    db: Session = Depends(get_db),
    user: Employee = Depends(oauth2.get_current_user),
    ) -> Any:
    current_user = await user
        
    invoice_for_customer_service = InvoiceForCustomerService(db=db)
    
    logger.info("Endpoints: get_invoice_for_customer_by_id called.")  
    msg, invoice_for_customer_response = await invoice_for_customer_service.get_invoice_for_customer_by_id(invoice_for_customer_id,current_user.tenant_id)
    logger.info("Endpoints: get_all_invoice_for_customers called successfully.")
    return make_response_object(invoice_for_customer_response, msg)
    
@router.put("/invoice_for_customers/{invoice_for_customer_id}")
async def update_invoice_for_customer(
    invoice_for_customer_id: str, 
    invoice_for_customer_update: InvoiceForCustomerUpdate, 
    db: Session = Depends(get_db),
    user: Employee = Depends(oauth2.get_current_user),
    ) -> Any:
    current_user = await user

        
    invoice_for_customer_service = InvoiceForCustomerService(db=db)
    
    logger.info("Endpoints: update_invoice_for_customer called.")
    msg, invoice_for_customer_response = await invoice_for_customer_service.update_invoice_for_customer(invoice_for_customer_id, invoice_for_customer_update, current_user.tenant_id)
    logger.info("Endpoints: update_invoice_for_customer called successfully.")
    return make_response_object(invoice_for_customer_response, msg)

@router.delete("/invoice_for_customers/{invoice_for_customer_id}")
async def delete_invoice_for_customer(
    invoice_for_customer_id: str, 
    user: Employee = Depends(oauth2.get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    current_user = await user
    
    invoice_for_customer_service = InvoiceForCustomerService(db=db)
    
    logger.info("Endpoints: delete_invoice_for_customer called.")
    msg, invoice_for_customer_response = await invoice_for_customer_service.delete_invoice_for_customer(invoice_for_customer_id,current_user.tenant_id)
    logger.info("Endpoints: delete_invoice_for_customer called successfully.")
    return make_response_object(invoice_for_customer_response, msg)
