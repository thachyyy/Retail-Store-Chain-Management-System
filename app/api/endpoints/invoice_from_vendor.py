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
from app.models import InvoiceFromVendor
from app.schemas.invoice_from_vendor import InvoiceFromVendorCreateParams, InvoiceFromVendorUpdate
from app.services.invoice_from_vendor import InvoiceFromVendorService
from app.utils.response import make_response_object
from app.models import Employee

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/invoice_from_vendor")
async def create_invoice_from_vendor(
    invoice_from_vendor_create: InvoiceFromVendorCreateParams,
    db: Session = Depends(get_db)
) -> Any:
    invoice_from_vendor_service = InvoiceFromVendorService(db=db)
    logger.info("Endpoints: create_invoice_from_vendor called.")
    
    msg, invoice_from_vendor_response = await invoice_from_vendor_service.create_invoice_from_vendor(invoice_from_vendor_create)
    logger.info("Endpoints: create_invoice_from_vendor called successfully.")
    return make_response_object(invoice_from_vendor_response, msg)

@router.get("/invoice_from_vendor")
async def get_all_invoice_from_vendor(db: Session = Depends(get_db)) -> Any:
    invoice_from_vendor_service = InvoiceFromVendorService(db=db)
    logger.info("Endpoints: get_all_invoice_from_vendor called.")
    
    msg, invoice_from_vendor_response = await invoice_from_vendor_service.get_all_invoice_from_vendors()
    logger.info("Endpoints: get_all_invoice_from_vendor called successfully.")
    return make_response_object(invoice_from_vendor_response, msg)

@router.get("/invoice_from_vendor/{invoice_from_vendor_id}")
async def get_invoice_from_vendor_by_id(invoice_from_vendor_id: str, db: Session = Depends(get_db)) -> Any:
    invoice_from_vendor_service = InvoiceFromVendorService(db=db)
    
    logger.info("Endpoints: get_invoice_from_vendor_by_id called.")  
    msg, invoice_from_vendor_response = await invoice_from_vendor_service.get_invoice_from_vendor_by_id(invoice_from_vendor_id)
    logger.info("Endpoints: get_all_invoice_from_vendor called successfully.")
    return make_response_object(invoice_from_vendor_response, msg)
    
@router.put("/invoice_from_vendor/{invoice_from_vendor_id}")
async def update_invoice_from_vendor(invoice_from_vendor_id: str, invoice_from_vendor_update: InvoiceFromVendorUpdate, db: Session = Depends(get_db)) -> Any:
    invoice_from_vendor_service = InvoiceFromVendorService(db=db)
    
    logger.info("Endpoints: update_invoice_from_vendor called.")
    msg, invoice_from_vendor_response = await invoice_from_vendor_service.update_invoice_from_vendor(invoice_from_vendor_id, invoice_from_vendor_update)
    logger.info("Endpoints: update_invoice_from_vendor called successfully.")
    return make_response_object(invoice_from_vendor_response, msg)

@router.delete("/invoice_from_vendor/{invoice_from_vendor_id}")
async def delete_invoice_from_vendor(invoice_from_vendor_id: str, db: Session = Depends(get_db)) -> Any:
    invoice_from_vendor_service = InvoiceFromVendorService(db=db)
    
    logger.info("Endpoints: delete_invoice_from_vendor called.")
    msg, invoice_from_vendor_response = await invoice_from_vendor_service.delete_invoice_from_vendor(invoice_from_vendor_id)
    logger.info("Endpoints: delete_invoice_from_vendor called successfully.")
    return make_response_object(invoice_from_vendor_response, msg)
