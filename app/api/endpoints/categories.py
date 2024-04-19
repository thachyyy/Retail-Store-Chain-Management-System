import logging

from typing import Any, Optional, Literal
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from pydantic import UUID4
from datetime import date

from app.api.depends import oauth2
# from app.api.depends.oauth2 import create_access_token, create_refresh_token, verify_refresh_token
from app.constant.app_status import AppStatus
from app.core.exceptions import error_exception_handler
from app.db.database import get_db
from app.schemas.categories import CategoriesCreateParams, CategoriesUpdate
from app.services.categories import CategoriesService
from app.utils.response import make_response_object
from app.models import Employee

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/categories")
async def create_categories(
    categories_create: CategoriesCreateParams,
    branch_name: Optional[str] = None,
    user: Employee = Depends(oauth2.get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    current_user = await user
    if current_user.role == "Nhân viên":
        raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_ACCESS_DENIED)
    
    if branch_name:
        branch = branch_name
    else:
        branch = current_user.branch
    
    categories_service = CategoriesService(db=db)
    logger.info("Endpoints: create_categories called.")
    
    msg, categories_response = await categories_service.create_categories(current_user.tenant_id, branch, categories_create)
    logger.info("Endpoints: create_categories called successfully.")
    return make_response_object(categories_response, msg)

@router.get("/categories")
async def get_all_categories(
    db: Session = Depends(get_db),
    branch_name: Optional[str] = None,
    user: Employee = Depends(oauth2.get_current_user),
    limit: Optional[int] = None,
    offset:Optional[int] = None,
    # sort: Literal['asc', 'desc'] = None
    ) -> Any:
    
    current_user = await user
    
    if branch_name:
        branch = branch_name
    else:
        branch = current_user.branch
    
    categories_service = CategoriesService(db=db)
    logger.info("Endpoints: get_all_categories called.")
    
    msg, categories_response = await categories_service.get_all_categories(tenant_id=current_user.tenant_id, branch=branch, limit=limit, offset=offset)
    logger.info("Endpoints: get_all_categories called successfully.")
    return make_response_object(categories_response, msg)

@router.get("/categories/{id}")
async def get_categories_by_id(
    id: str, 
    db: Session = Depends(get_db),
    branch_name: Optional[str] = None,
    user: Employee = Depends(oauth2.get_current_user),
) -> Any:
    
    current_user = await user
    
    if branch_name:
        branch = branch_name
    else:
        branch = current_user.branch
    
    categories_service = CategoriesService(db=db)
    
    logger.info("Endpoints: get_categories_by_id called.")  
    msg, categories_response = await categories_service.get_categories_by_id(current_user.tenant_id, branch, id)
    logger.info("Endpoints: get_categories_by_id called successfully.")
    return make_response_object(categories_response, msg)

@router.put("/categories/{id}")
async def update_categories(
    id: str, 
    categories_update: CategoriesUpdate, 
    db: Session = Depends(get_db),
    branch_name: Optional[str] = None,
    user: Employee = Depends(oauth2.get_current_user),
) -> Any:
    current_user = await user
    
    if current_user.role == "Nhân viên":
        raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_ACCESS_DENIED)
    
    if branch_name:
        branch = branch_name
    else:
        branch = current_user.branch
    
    categories_service = CategoriesService(db=db)
    
    logger.info("Endpoints: update_categories called.")
    msg, categories_response = await categories_service.update_categories(current_user.tenant_id, branch, id, categories_update)
    logger.info("Endpoints: update_categories called successfully.")
    return make_response_object(categories_response, msg)

@router.delete("/categories/{id}")
async def delete_categories(
    id: str, 
    db: Session = Depends(get_db),
    branch_name: Optional[str] = None,
    user: Employee = Depends(oauth2.get_current_user),
) -> Any:
    
    current_user = await user
    
    if current_user.role == "Nhân viên":
        raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_ACCESS_DENIED)
    
    if branch_name:
        branch = branch_name
    else:
        branch = current_user.branch
    
    categories_service = CategoriesService(db=db)
    
    logger.info("Endpoints: delete_categories called.")
    msg, categories_response = await categories_service.delete_categories(current_user.tenant_id, branch, id)
    logger.info("Endpoints: delete_categories called successfully.")
    return make_response_object(categories_response, msg)