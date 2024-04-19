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
from app.schemas.promotion import PromotionCreateParams, PromotionUpdate
from app.services.promotion import PromotionService
from app.utils.response import make_response_object
from app.models import Employee

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/promotions")
async def create_promotion(
    promotion_create: PromotionCreateParams,
    user: Employee = Depends(oauth2.get_current_user),
    branch_name: str = None,
    db: Session = Depends(get_db)
) -> Any:
    current_user = await user
    
    if current_user.role == "Nhân viên":
        raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_ACCESS_DENIED)
    
    if branch_name:
        branch = branch_name
    else:
        branch = current_user.branch
        
    
    promotion_service = PromotionService(db=db)
    logger.info("Endpoints: create_promotion called.")
    
    promotion_response = await promotion_service.create_promotion(promotion_create, current_user.tenant_id, branch)
    logger.info("Endpoints: create_promotion called successfully.")
    return make_response_object(promotion_response)

@router.get("/promotions")
async def get_all_promotions(
    user: Employee = Depends(oauth2.get_current_user),
    branch_name: Optional[str] = None,
    db: Session = Depends(get_db)
) -> Any:
    current_user = await user
    
    if branch_name:
        branch = branch_name
    else:
        branch = current_user.branch
    
    promotion_service = PromotionService(db=db)
    logger.info("Endpoints: get_all_promotions called.")
    
    msg, promotion_response = await promotion_service.get_all_promotions(current_user.tenant_id, branch)
    logger.info("Endpoints: get_all_promotions called successfully.")
    return make_response_object(promotion_response, msg)

@router.get("/promotions/{promotion_id}")
async def get_promotion_by_id(
    promotion_id: str, 
    db: Session = Depends(get_db),
    user: Employee = Depends(oauth2.get_current_user),
) -> Any:
    
    current_user = await user
    
    promotion_service = PromotionService(db=db)
    
    logger.info("Endpoints: get_promotion_by_id called.")  
    msg, promotion_response = await promotion_service.get_promotion_by_id(promotion_id, current_user.tenant_id)
    logger.info("Endpoints: get_all_promotions called successfully.")
    return make_response_object(promotion_response, msg)
    
@router.put("/promotions/{promotion_id}")
async def update_promotion(
    promotion_id: str, 
    promotion_update: PromotionUpdate, 
    db: Session = Depends(get_db),
    user: Employee = Depends(oauth2.get_current_user),
) -> Any:
    current_user = await user
    
    if current_user.role == "Nhân viên":
        raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_ACCESS_DENIED) 
    
    promotion_service = PromotionService(db=db)
    
    logger.info("Endpoints: update_promotion called.")
    msg, promotion_response = await promotion_service.update_promotion(promotion_id, promotion_update, current_user.tenant_id)
    logger.info("Endpoints: update_promotion called successfully.")
    return make_response_object(promotion_response, msg)

@router.delete("/promotions/{promotion_id}")
async def delete_promotion(
    promotion_id: str, 
    db: Session = Depends(get_db),
    user: Employee = Depends(oauth2.get_current_user),
) -> Any:
    current_user = await user
    if current_user.role == "Nhân viên":
        raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_ACCESS_DENIED) 
    
    promotion_service = PromotionService(db=db)
    
    logger.info("Endpoints: delete_promotion called.")
    msg, promotion_response = await promotion_service.delete_promotion(promotion_id,current_user.tenant_id)
    logger.info("Endpoints: delete_promotion called successfully.")
    return make_response_object(promotion_response, msg)

@router.get("promotions/search")
async def search_promotion(db: Session = Depends(get_db), condition: Optional[str] = Query(None)) -> Any:
    promotion_service = PromotionService(db=db)
    
    logger.info("Endpoints: search_promotion called.")
    msg, promotion_response = await promotion_service.search_promotion(condition)
    logger.info("Endpoints: search_promotion called successfully.")
    
    return make_response_object(promotion_response, msg)

@router.get("promotions/filter")
async def filter_promotion(
    db: Session = Depends(get_db),
    status: str = None,
) -> Any:
    promotion_service = PromotionService(db=db)
    
    logger.info("Endpoints: filter_promotion called.")
    msg, promotion_response = await promotion_service.filter_promotion(status)
    logger.info("Endpoints: filter_promotion called successfully.")
    
    return make_response_object(promotion_response, msg)