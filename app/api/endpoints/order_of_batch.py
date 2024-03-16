import logging

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Any, Optional

from app.db.database import get_db
from app.services.order_of_batch import OrderOfBatchService
from app.utils.response import make_response_object
from app.schemas.order_of_batch import OrderOfBatchCreateParams, OrderOfBatchUpdate



logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/order_of_batches")
async def get_all_order_of_batches(db: Session = Depends(get_db)) -> Any:
    order_of_batch_service = OrderOfBatchService(db=db)
    logger.info("Endpoints: get_all_order_of_batches called.")
    
    msg, order_of_batch_response = await order_of_batch_service.get_all_order_of_batches()
    logger.info("Endpoints: get_all_order_of_batches called successfully.")
    return make_response_object(order_of_batch_response, msg)

@router.get("/order_of_batches/{order_of_batch_id}")
async def get_order_of_batch_by_id(order_of_batch_id: str, db: Session = Depends(get_db)) -> Any:
    order_of_batch_service = OrderOfBatchService(db=db)
    
    logger.info("Endpoints: get_order_of_batch_by_id called.")  
    msg, order_of_batch_response = await order_of_batch_service.get_order_of_batch_by_id(order_of_batch_id)
    logger.info("Endpoints: get_all_order_of_batchs called successfully.")
    return make_response_object(order_of_batch_response, msg)

@router.post("/order_of_batches")
async def create_order_of_batch(
    order_of_batch_create: OrderOfBatchCreateParams,
    db: Session = Depends(get_db)
) -> Any:
    order_of_batch_service = OrderOfBatchService(db=db)
    logger.info("Endpoints: create_order_of_batch called.")
    
    msg, order_of_batch_response = await order_of_batch_service.create_order_of_batch(order_of_batch_create)
    logger.info("Endpoints: create_order_of_batch called successfully.")
    return make_response_object(order_of_batch_response, msg)

@router.put("/order_of_batches/{order_of_batch_id}")
async def update_order_of_batch(order_of_batch_id: str, order_of_batch_update: OrderOfBatchUpdate, db: Session = Depends(get_db)) -> Any:
    order_of_batch_service = OrderOfBatchService(db=db)
    
    logger.info("Endpoints: update_order_of_batch called.")
    msg, order_of_batch_response = await order_of_batch_service.update_order_of_batch(order_of_batch_id, order_of_batch_update)
    logger.info("Endpoints: update_order_of_batch called successfully.")
    return make_response_object(order_of_batch_response, msg)

@router.delete("/order_of_batches/{order_of_batch_id}")
async def delete_order_of_batch(order_of_batch_id: str, db: Session = Depends(get_db)) -> Any:
    order_of_batch_service = OrderOfBatchService(db=db)
    
    logger.info("Endpoints: delete_order_of_batch called.")
    msg, order_of_batch_response = await order_of_batch_service.delete_order_of_batch(order_of_batch_id)
    logger.info("Endpoints: delete_order_of_batch called successfully.")
    return make_response_object(order_of_batch_response, msg)
