import logging

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Any, Optional

from app.db.database import get_db
from app.services.vendor import VendorService
from app.utils.response import make_response_object
from app.schemas.vendor import VendorCreateParams, VendorUpdate



logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/vendors")
async def get_all_vendors(db: Session = Depends(get_db)) -> Any:
    vendor_service = VendorService(db=db)
    logger.info("Endpoints: get_all_vendors called.")
    
    msg, vendor_response = await vendor_service.get_all_vendors()
    logger.info("Endpoints: get_all_vendors called successfully.")
    return make_response_object(vendor_response, msg)

@router.get("/vendors/{vendor_id}")
async def get_vendor_by_id(vendor_id: str, db: Session = Depends(get_db)) -> Any:
    vendor_service = VendorService(db=db)
    
    logger.info("Endpoints: get_vendor_by_id called.")  
    msg, vendor_response = await vendor_service.get_vendor_by_id(vendor_id)
    logger.info("Endpoints: get_all_vendors called successfully.")
    return make_response_object(vendor_response, msg)

@router.post("/vendors")
async def create_vendor(
    vendor_create: VendorCreateParams,
    db: Session = Depends(get_db)
) -> Any:
    vendor_service = VendorService(db=db)
    logger.info("Endpoints: create_vendor called.")
    
    vendor_response = await vendor_service.create_vendor(vendor_create)
    logger.info("Endpoints: create_vendor called successfully.")
    return make_response_object(vendor_response)

@router.put("/vendors/{vendor_id}")
async def update_vendor(vendor_id: str, vendor_update: VendorUpdate, db: Session = Depends(get_db)) -> Any:
    vendor_service = VendorService(db=db)
    
    logger.info("Endpoints: update_vendor called.")
    msg, vendor_response = await vendor_service.update_vendor(vendor_id, vendor_update)
    logger.info("Endpoints: update_vendor called successfully.")
    return make_response_object(vendor_response, msg)

@router.delete("/vendors/{vendor_id}")
async def delete_vendor(vendor_id: str, db: Session = Depends(get_db)) -> Any:
    vendor_service = VendorService(db=db)
    
    logger.info("Endpoints: delete_vendor called.")
    msg, vendor_response = await vendor_service.delete_vendor(vendor_id)
    logger.info("Endpoints: delete_vendor called successfully.")
    return make_response_object(vendor_response, msg)

@router.get("vendors/search")
async def search_vendor(db: Session = Depends(get_db), condition: Optional[str] = Query(None)) -> Any:
    vendor_service = VendorService(db=db)
    
    logger.info("Endpoints: search_vendor called.")
    msg, vendor_response = await vendor_service.search_vendor(condition)
    logger.info("Endpoints: search_vendor called successfully.")
    
    return make_response_object(vendor_response, msg)