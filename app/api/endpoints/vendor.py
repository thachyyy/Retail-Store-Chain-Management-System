import logging

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Any, Optional

from app.db.database import get_db
from app.api.depends import oauth2
from app.constant.app_status import AppStatus
from app.core.exceptions import error_exception_handler
from app.services.vendor import VendorService
from app.utils.response import make_response_object
from app.schemas.vendor import VendorCreateParams, VendorUpdate
from app.models import Employee



logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/vendors")
async def get_all_vendors(
    user: Employee = Depends(oauth2.get_current_user),
    db: Session = Depends(get_db),
    limit: int = None,
    offset: int = None,
    province: str = None,
    district: str = None,
    status: str = None,
    id: str = None,
    vendor_name: str = None,
    company_name: str = None,
    email: str = None,
    phone_number: str = None,
    address: str = None,
    note: str = None,
    query_search: Optional[str] = None,
) -> Any:
    
    current_user = await user
    
    if current_user.role == "Nhân viên":
        raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_ACCESS_DENIED)
    
    vendor_service = VendorService(db=db)
    logger.info("Endpoints: get_all_vendors called.")
    
    msg, vendor_response = await vendor_service.get_all_vendors(
        current_user.tenant_id,
        limit,
        offset,
        province,
        district,
        status,
        id,
        vendor_name,
        company_name,
        email,
        phone_number,
        address,
        note,
        query_search
    )
    logger.info("Endpoints: get_all_vendors called successfully.")
    return make_response_object(vendor_response, msg)

@router.get("/vendors/{vendor_id}")
async def get_vendor_by_id(
    vendor_id: str, 
    db: Session = Depends(get_db),
    user: Employee = Depends(oauth2.get_current_user),
) -> Any:
    
    current_user = await user
    if current_user.role == "Nhân viên":
        raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_ACCESS_DENIED)
    
    vendor_service = VendorService(db=db)
    
    logger.info("Endpoints: get_vendor_by_id called.")  
    msg, vendor_response = await vendor_service.get_vendor_by_id(current_user.tenant_id, vendor_id)
    logger.info("Endpoints: get_all_vendors called successfully.")
    return make_response_object(vendor_response, msg)

@router.post("/vendors")
async def create_vendor(
    vendor_create: VendorCreateParams,
    db: Session = Depends(get_db),
    user: Employee = Depends(oauth2.get_current_user),
) -> Any:
    
    current_user = await user
    if current_user.role != "Quản lý":
        raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_ACCESS_DENIED)
    
    vendor_service = VendorService(db=db)
    logger.info("Endpoints: create_vendor called.")
    
    msg,vendor_response = await vendor_service.create_vendor(current_user.tenant_id,vendor_create)
    logger.info("Endpoints: create_vendor called successfully.")
    return make_response_object(vendor_response,msg)

@router.put("/vendors/{vendor_id}")
async def update_vendor(
    vendor_id: str, 
    vendor_update: VendorUpdate, 
    db: Session = Depends(get_db),
    user: Employee = Depends(oauth2.get_current_user),
) -> Any:
    
    current_user = await user
    if current_user.role != "Quản lý":
        raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_ACCESS_DENIED)
    
    vendor_service = VendorService(db=db)
    
    logger.info("Endpoints: update_vendor called.")
    msg, vendor_response = await vendor_service.update_vendor(current_user.tenant_id, vendor_id, vendor_update)
    logger.info("Endpoints: update_vendor called successfully.")
    return make_response_object(vendor_response, msg)

@router.delete("/vendors/{vendor_id}")
async def delete_vendor(
    vendor_id: str, 
    db: Session = Depends(get_db),
    user: Employee = Depends(oauth2.get_current_user),
) -> Any:
    
    current_user = await user
    if current_user.role != "Quản lý":
        raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_ACCESS_DENIED)
    
    vendor_service = VendorService(db=db)
    
    logger.info("Endpoints: delete_vendor called.")
    msg, vendor_response = await vendor_service.delete_vendor(current_user.tenant_id, vendor_id)
    logger.info("Endpoints: delete_vendor called successfully.")
    return make_response_object(vendor_response, msg)

# @router.get("vendor/search")
# async def search_vendor(
#     db: Session = Depends(get_db), 
#     condition: Optional[str] = Query(None),
#     limit: Optional[int] = None,
#     offset:Optional[int] = None
# ) -> Any:
#     vendor_service = VendorService(db=db)
    
#     logger.info("Endpoints: search_vendor called.")
#     msg, vendor_response = await vendor_service.search_vendor(condition, limit, offset)
#     logger.info("Endpoints: search_vendor called successfully.")
    
#     return make_response_object(vendor_response, msg)