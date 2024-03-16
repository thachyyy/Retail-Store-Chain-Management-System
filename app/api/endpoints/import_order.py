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
from app.schemas.import_order import ImportOrderCreateParams, ImportOrderUpdate
from app.services.import_order import ImportOrderService
from app.utils.response import make_response_object

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/import_order")
async def create_import_order(
    import_order_create: ImportOrderCreateParams,
    db: Session = Depends(get_db)
) -> Any:
    import_order_service = ImportOrderService(db=db)
    logger.info("Endpoints: create_import_order called.")
    
    msg, import_order_response = await import_order_service.create_import_order(import_order_create)
    logger.info("Endpoints: create_import_order called successfully.")
    return make_response_object(import_order_response, msg)

@router.get("/import_orders")
async def get_all_import_order(db: Session = Depends(get_db)) -> Any:
    import_order_service = ImportOrderService(db=db)
    logger.info("Endpoints: get_all_import_orders called.")
    
    msg, import_order_response = await import_order_service.get_all_import_orders()
    logger.info("Endpoints: get_all_import_orders called successfully.")
    return make_response_object(import_order_response, msg)

@router.get("/import_orders/{id}")
async def get_import_order_by_id(id: str, db: Session = Depends(get_db)) -> Any:
    import_order_service = ImportOrderService(db=db)
    
    logger.info("Endpoints: get_import_order_by_id called.")  
    msg, import_order_response = await import_order_service.get_import_order_by_id(id)
    logger.info("Endpoints: get_import_order_by_id called successfully.")
    return make_response_object(import_order_response, msg)

@router.put("/import_orders/{id}")
async def update_import_order(id: str, import_order_update: ImportOrderUpdate, db: Session = Depends(get_db)) -> Any:
    import_order_service = ImportOrderService(db=db)
    
    logger.info("Endpoints: update_import_order called.")
    msg, import_order_response = await import_order_service.update_import_order(id, import_order_update)
    logger.info("Endpoints: update_import_order called successfully.")
    return make_response_object(import_order_response, msg)

@router.delete("/import_orders/{id}")
async def delete_import_order(id: str, db: Session = Depends(get_db)) -> Any:
    import_order_service = ImportOrderService(db=db)
    
    logger.info("Endpoints: delete_import_order called.")
    msg, import_order_response = await import_order_service.delete_import_order(id)
    logger.info("Endpoints: delete_import_order called successfully.")
    return make_response_object(import_order_response, msg)