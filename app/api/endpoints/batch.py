import logging

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Any, Optional

from app.db.database import get_db
from app.services.batch import BatchService
from app.utils.response import make_response_object
from app.schemas.batch import BatchCreateParams, BatchUpdate



logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/batches")
async def get_all_batches(
    db: Session = Depends(get_db),
    limit: Optional[int] = None,
    offset:Optional[int] = None,
) -> Any:
    batch_service = BatchService(db=db)
    logger.info("Endpoints: get_all_batches called.")
    
    msg, batch_response = await batch_service.get_all_batches(limit=limit, offset=offset)
    logger.info("Endpoints: get_all_batches called successfully.")
    return make_response_object(batch_response, msg)

@router.get("/batches/{batch_id}")
async def get_batch_by_id(batch_id: str, db: Session = Depends(get_db)) -> Any:
    batch_service = BatchService(db=db)
    
    logger.info("Endpoints: get_batch_by_id called.")  
    msg, batch_response = await batch_service.get_batch_by_id(batch_id)
    logger.info("Endpoints: get_batch_by_id called successfully.")
    return make_response_object(batch_response, msg)

@router.get("/batches_product/{product_id}")
async def get_batch_by_product_id(product_id: str, db: Session = Depends(get_db)) -> Any:
    batch_service = BatchService(db=db)
    
    logger.info("Endpoints: get_batch_by_prod_id called.")  
    msg, batch_response = await batch_service.get_batch_by_product_id(product_id)
    logger.info("Endpoints: get_batch_by_prod_id called successfully.")
    return make_response_object(batch_response, msg)

@router.post("/batches")
async def create_batch(
    batch_create: BatchCreateParams,
    db: Session = Depends(get_db)
) -> Any:
    batch_service = BatchService(db=db)
    logger.info("Endpoints: create_batch called.")
    
    msg, batch_response = await batch_service.create_batch(batch_create)
    logger.info("Endpoints: create_batch called successfully.")
    return make_response_object(batch_response, msg)

@router.put("/batches/{batch_id}")
async def update_batch(batch_id: str, batch_update: BatchUpdate, db: Session = Depends(get_db)) -> Any:
    batch_service = BatchService(db=db)
    
    logger.info("Endpoints: update_batch called.")
    msg, batch_response = await batch_service.update_batch(batch_id, batch_update)
    logger.info("Endpoints: update_batch called successfully.")
    return make_response_object(batch_response, msg)

@router.put("/batches/update_quantity/{batch_id}")
async def update_batch(batch_id: str,quantity:int, db: Session = Depends(get_db)) -> Any:
    batch_service = BatchService(db=db)
    print("dfasdf",quantity)
    logger.info("Endpoints: update_batch called.")
    msg, batch_response = await batch_service.update_quantity(batch_id, quantity)
    logger.info("Endpoints: update_batch called successfully.")
    return make_response_object(batch_response, msg)

@router.delete("/batches/{batch_id}")
async def delete_batch(batch_id: str, db: Session = Depends(get_db)) -> Any:
    batch_service = BatchService(db=db)
    
    logger.info("Endpoints: delete_batch called.")
    msg, batch_response = await batch_service.delete_batch(batch_id)
    logger.info("Endpoints: delete_batch called successfully.")
    return make_response_object(batch_response, msg)
