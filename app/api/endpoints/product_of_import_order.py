import logging

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Any, Optional

from app.db.database import get_db
from app.services.product_of_import_order import ProductOfImportOrderService
from app.utils.response import make_response_object
from app.schemas.product_of_import_order import ProductOfImportOrderCreateParams, ProductOfImportOrderUpdate



logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/product_of_import_orders")
async def get_all_product_of_import_orders(db: Session = Depends(get_db)) -> Any:
    product_of_import_order_service = ProductOfImportOrderService(db=db)
    logger.info("Endpoints: get_all_product_of_import_orderes called.")
    
    msg, product_of_import_order_response = await product_of_import_order_service.get_all_product_of_import_orders()
    logger.info("Endpoints: get_all_product_of_import_orderes called successfully.")
    return make_response_object(product_of_import_order_response, msg)

@router.get("/product_of_import_orderes/{product_of_import_order_id}")
async def get_product_of_import_order_by_id(product_of_import_order_id: str, db: Session = Depends(get_db)) -> Any:
    product_of_import_order_service = ProductOfImportOrderService(db=db)
    
    logger.info("Endpoints: get_product_of_import_order_by_id called.")  
    msg, product_of_import_order_response = await product_of_import_order_service.get_product_of_import_order_by_id(product_of_import_order_id)
    logger.info("Endpoints: get_all_product_of_import_orders called successfully.")
    return make_response_object(product_of_import_order_response, msg)

@router.post("/product_of_import_orderes")
async def create_product_of_import_order(
    product_of_import_order_create: ProductOfImportOrderCreateParams,
    db: Session = Depends(get_db)
) -> Any:
    product_of_import_order_service = ProductOfImportOrderService(db=db)
    logger.info("Endpoints: create_product_of_import_order called.")
    
    msg, product_of_import_order_response = await product_of_import_order_service.create_product_of_import_order(product_of_import_order_create)
    logger.info("Endpoints: create_product_of_import_order called successfully.")
    return make_response_object(product_of_import_order_response, msg)

@router.put("/product_of_import_orderes/{product_of_import_order_id}")
async def update_product_of_import_order(product_of_import_order_id: str, product_of_import_order_update: ProductOfImportOrderUpdate, db: Session = Depends(get_db)) -> Any:
    product_of_import_order_service = ProductOfImportOrderService(db=db)
    
    logger.info("Endpoints: update_product_of_import_order called.")
    msg, product_of_import_order_response = await product_of_import_order_service.update_product_of_import_order(product_of_import_order_id, product_of_import_order_update)
    logger.info("Endpoints: update_product_of_import_order called successfully.")
    return make_response_object(product_of_import_order_response, msg)

@router.delete("/product_of_import_orderes/{product_of_import_order_id}")
async def delete_product_of_import_order(product_of_import_order_id: str, db: Session = Depends(get_db)) -> Any:
    product_of_import_order_service = ProductOfImportOrderService(db=db)
    
    logger.info("Endpoints: delete_product_of_import_order called.")
    msg, product_of_import_order_response = await product_of_import_order_service.delete_product_of_import_order(product_of_import_order_id)
    logger.info("Endpoints: delete_product_of_import_order called successfully.")
    return make_response_object(product_of_import_order_response, msg)
