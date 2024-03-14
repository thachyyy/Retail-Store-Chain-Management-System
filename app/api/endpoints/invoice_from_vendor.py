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
from app.models import InvoiceForVendor
from app.schemas import ChangePassword, InvoiceForVendorResponse
from app.schemas.invoice_for_vendor import InvoiceForVendorCreateParams, InvoiceForVendorUpdate
from app.services.invoice_for_vendor import InvoiceForVendorService
from app.utils.response import make_response_object

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/invoice_for_vendor")
async def create_invoice_for_vendor(
    invoice_for_vendor_create: InvoiceForVendorCreateParams,
    db: Session = Depends(get_db)
) -> Any:
    invoice_for_vendor_service = InvoiceForVendorService(db=db)
    logger.info("Endpoints: create_invoice_for_vendor called.")
    
    msg, invoice_for_vendor_response = await invoice_for_vendor_service.create_invoice_for_vendor(invoice_for_vendor_create)
    logger.info("Endpoints: create_invoice_for_vendor called successfully.")
    return make_response_object(invoice_for_vendor_response)

@router.get("/invoice_for_vendor")
async def get_all_invoice_for_vendor(db: Session = Depends(get_db)) -> Any:
    invoice_for_vendor_service = InvoiceForVendorService(db=db)
    logger.info("Endpoints: get_all_invoice_for_vendor called.")
    
    msg, invoice_for_vendor_response = await invoice_for_vendor_service.get_all_invoice_for_vendor()
    logger.info("Endpoints: get_all_invoice_for_vendor called successfully.")
    return make_response_object(invoice_for_vendor_response, msg)

@router.get("/invoice_for_vendor/{invoice_for_vendor_id}")
async def get_invoice_for_vendor_by_id(invoice_for_vendor_id: str, db: Session = Depends(get_db)) -> Any:
    invoice_for_vendor_service = InvoiceForVendorService(db=db)
    
    logger.info("Endpoints: get_invoice_for_vendor_by_id called.")  
    msg, invoice_for_vendor_response = await invoice_for_vendor_service.get_invoice_for_vendor_by_id(invoice_for_vendor_id)
    logger.info("Endpoints: get_all_invoice_for_vendor called successfully.")
    return make_response_object(invoice_for_vendor_response, msg)
    
@router.put("/invoice_for_vendor/{invoice_for_vendor_id}")
async def update_invoice_for_vendor(invoice_for_vendor_id: str, invoice_for_vendor_update: InvoiceForVendorUpdate, db: Session = Depends(get_db)) -> Any:
    invoice_for_vendor_service = InvoiceForVendorService(db=db)
    
    logger.info("Endpoints: update_invoice_for_vendor called.")
    msg, invoice_for_vendor_response = await invoice_for_vendor_service.update_invoice_for_vendor(invoice_for_vendor_id, invoice_for_vendor_update)
    logger.info("Endpoints: update_invoice_for_vendor called successfully.")
    return make_response_object(invoice_for_vendor_response, msg)

@router.delete("/invoice_for_vendor/{invoice_for_vendor_id}")
async def delete_invoice_for_vendor(invoice_for_vendor_id: str, db: Session = Depends(get_db)) -> Any:
    invoice_for_vendor_service = InvoiceForVendorService(db=db)
    
    logger.info("Endpoints: delete_invoice_for_vendor called.")
    msg, invoice_for_vendor_response = await invoice_for_vendor_service.delete_invoice_for_vendor(invoice_for_vendor_id)
    logger.info("Endpoints: delete_invoice_for_vendor called successfully.")
    return make_response_object(invoice_for_vendor_response, msg)
