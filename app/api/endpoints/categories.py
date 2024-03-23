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

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/categories")
async def create_categories(
    categories_create: CategoriesCreateParams,
    db: Session = Depends(get_db)
) -> Any:
    categories_service = CategoriesService(db=db)
    logger.info("Endpoints: create_categories called.")
    
    msg, categories_response = await categories_service.create_categories(categories_create)
    logger.info("Endpoints: create_categories called successfully.")
    return make_response_object(categories_response, msg)

@router.get("/categories")
async def get_all_categories(
    db: Session = Depends(get_db),
    limit: Optional[int] = None,
    offset:Optional[int] = None,
    sort: Literal['asc', 'desc'] = None
    ) -> Any:
    categories_service = CategoriesService(db=db)
    logger.info("Endpoints: get_all_categories called.")
    
    msg, categories_response = await categories_service.get_all_categories(limit=limit, offset=offset, sort=sort)
    logger.info("Endpoints: get_all_categories called successfully.")
    return make_response_object(categories_response, msg)

@router.get("/categories/{id}")
async def get_categories_by_id(id: str, db: Session = Depends(get_db)) -> Any:
    categories_service = CategoriesService(db=db)
    
    logger.info("Endpoints: get_categories_by_id called.")  
    msg, categories_response = await categories_service.get_categories_by_id(id)
    logger.info("Endpoints: get_categories_by_id called successfully.")
    return make_response_object(categories_response, msg)

@router.put("/categories/{id}")
async def update_categories(id: str, categories_update: CategoriesUpdate, db: Session = Depends(get_db)) -> Any:
    categories_service = CategoriesService(db=db)
    
    logger.info("Endpoints: update_categories called.")
    msg, categories_response = await categories_service.update_categories(id, categories_update)
    logger.info("Endpoints: update_categories called successfully.")
    return make_response_object(categories_response, msg)

@router.delete("/categories/{id}")
async def delete_categories(id: str, db: Session = Depends(get_db)) -> Any:
    categories_service = CategoriesService(db=db)
    
    logger.info("Endpoints: delete_categories called.")
    msg, categories_response = await categories_service.delete_categories(id)
    logger.info("Endpoints: delete_categories called successfully.")
    return make_response_object(categories_response, msg)