import logging

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Any, Optional

from app.api.depends import oauth2
from app.db.database import get_db
from app.services.batch import BatchService
from app.utils.response import make_response_object
from app.schemas.batch import BatchCreateParams, BatchUpdate
from app.models import Employee


logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/batches")
async def get_all_batches(
    db: Session = Depends(get_db),
    user: Employee = Depends(oauth2.get_current_user),
    branch_id: Optional[str] = None,
    limit: Optional[int] = None,
    offset:Optional[int] = None,
) -> Any:
    
    current_user = await user
    
    batch_service = BatchService(db=db)
    logger.info("Endpoints: get_all_batches called.")
    
    if branch_id:
        msg, batch_response = await batch_service.get_all_batches(
            tenant_id=current_user.tenant_id,
            branch=branch_id,
            limit=limit, 
            offset=offset
        )
    else:
        msg, batch_response = await batch_service.get_all_batches(
            tenant_id=current_user.tenant_id,
            branch=current_user.branch,
            limit=limit, 
            offset=offset
        )
    logger.info("Endpoints: get_all_batches called successfully.")
    return make_response_object(batch_response, msg)

@router.get("/batches/{batch_id}")
async def get_batch_by_id(
    batch_id: str,
    user: Employee = Depends(oauth2.get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    
    current_user = await user
    batch_service = BatchService(db=db)
    
    logger.info("Endpoints: get_batch_by_id called.")  
    msg, batch_response = await batch_service.get_batch_by_id(batch_id, current_user.tenant_id)
    logger.info("Endpoints: get_batch_by_id called successfully.")
    return make_response_object(batch_response, msg)

@router.get("/batches_product/{product_id}")
async def get_batch_by_product_id(
    product_id: str, 
    user: Employee = Depends(oauth2.get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    current_user = await user
    batch_service = BatchService(db=db)
    
    logger.info("Endpoints: get_batch_by_prod_id called.")  
    msg, batch_response = await batch_service.get_batch_by_product_id(product_id, current_user.tenant_id)
    logger.info("Endpoints: get_batch_by_prod_id called successfully.")
    return make_response_object(batch_response, msg)

@router.post("/batches")
async def create_batch(
    batch_create: BatchCreateParams,
    user: Employee = Depends(oauth2.get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    current_user = await user
    batch_service = BatchService(db=db)
    logger.info("Endpoints: create_batch called.")
    
    msg, batch_response = await batch_service.create_batch(batch_create, current_user.tenant_id, current_user.branch_id)
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
