import logging

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Any, Optional

from app.api.depends import oauth2
from app.constant.app_status import AppStatus
from app.core.exceptions import error_exception_handler
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
    branch: Optional[str] = None,
    limit: Optional[int] = None,
    offset:Optional[int] = None,
    query_search: Optional[str] = None
) -> Any:
    
    current_user = await user
    
    batch_service = BatchService(db=db)
    logger.info("Endpoints: get_all_batches called.")
    
    if current_user.branch:
        branch = current_user.branch
    else:
        branch = branch
    
    msg, batch_response = await batch_service.get_all_batches(
            tenant_id=current_user.tenant_id,
            branch=branch,
            limit=limit, 
            offset=offset,
            query_search = query_search)
   
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
    
    msg, batch_response = await batch_service.create_batch(batch_create, current_user.tenant_id, current_user.branch)
    logger.info("Endpoints: create_batch called successfully.")
    return make_response_object(batch_response, msg)

@router.put("/batches/{batch_id}")
async def update_batch(
    batch_id: str, 
    batch_update: BatchUpdate, 
    user: Employee = Depends(oauth2.get_current_user),
    db: Session = Depends(get_db)) -> Any:
    
    current_user = await user
    if current_user.role == "Nhân viên":
        raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_ACCESS_DENIED)
    
    batch_service = BatchService(db=db)
    
    logger.info("Endpoints: update_batch called.")
    msg, batch_response = await batch_service.update_batch(batch_id, batch_update,current_user.tenant_id)
    logger.info("Endpoints: update_batch called successfully.")
    return make_response_object(batch_response, msg)

@router.put("/batches/update_quantity/{batch_id}")
async def update_batch(batch_id: str,quantity:int,tenant_id:str ,db: Session = Depends(get_db)) -> Any:
    batch_service = BatchService(db=db)
    
    logger.info("Endpoints: update_batch called.")
    msg, batch_response = await batch_service.update_quantity(batch_id, quantity,tenant_id)
    logger.info("Endpoints: update_batch called successfully.")
    return make_response_object(batch_response, msg)

@router.delete("/batches/{batch_id}")
async def delete_batch(batch_id: str, db: Session = Depends(get_db)) -> Any:
    batch_service = BatchService(db=db)
    
    logger.info("Endpoints: delete_batch called.")
    msg, batch_response = await batch_service.delete_batch(batch_id)
    logger.info("Endpoints: delete_batch called successfully.")
    return make_response_object(batch_response, msg)
