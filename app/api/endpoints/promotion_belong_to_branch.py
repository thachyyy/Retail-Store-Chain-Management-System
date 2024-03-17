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
from app.schemas.promotion_belong_to_branch import PromotionBelongToBranchCreateParams, PromotionBelongToBranchUpdate
from app.services.promotion_belong_to_branch import PromotionBelongToBranchService
from app.utils.response import make_response_object

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/promotions_belong_to_branch")
async def create_promotion_belong_to_branch(
    promotion_belong_to_branch_create: PromotionBelongToBranchCreateParams,
    db: Session = Depends(get_db)
) -> Any:
    promotion_belong_to_branch_service = PromotionBelongToBranchService(db=db)
    logger.info("Endpoints: create_promotion_belong_to_branch called.")
    
    promotion_belong_to_branch_response = await promotion_belong_to_branch_service.create_promotion_belong_to_branch(promotion_belong_to_branch_create)
    logger.info("Endpoints: create_promotion_belong_to_branch called successfully.")
    return make_response_object(promotion_belong_to_branch_response)

@router.get("/promotions_belong_to_branch")
async def get_all_promotions_belong_to_branch(db: Session = Depends(get_db)) -> Any:
    promotion_belong_to_branch_service = PromotionBelongToBranchService(db=db)
    logger.info("Endpoints: get_all_promotions_belong_to_branch called.")
    
    msg, promotion_belong_to_branch_response = await promotion_belong_to_branch_service.get_all_promotions_belong_to_branch()
    logger.info("Endpoints: get_all_promotions_belong_to_branch called successfully.")
    return make_response_object(promotion_belong_to_branch_response, msg)

@router.get("/promotions_belong_to_branch/{promotion_belong_to_branch_id}")
async def get_promotion_belong_to_branch_by_id(promotion_belong_to_branch_id: str, db: Session = Depends(get_db)) -> Any:
    promotion_belong_to_branch_service = PromotionBelongToBranchService(db=db)
    
    logger.info("Endpoints: get_promotion_belong_to_branch_by_id called.")  
    msg, promotion_belong_to_branch_response = await promotion_belong_to_branch_service.get_promotion_belong_to_branch_by_id(promotion_belong_to_branch_id)
    logger.info("Endpoints: get_all_promotion_belong_to_branchs called successfully.")
    return make_response_object(promotion_belong_to_branch_response, msg)
    
@router.put("/promotions_belong_to_branch/{promotion_belong_to_branch_id}")
async def update_promotion_belong_to_branch(promotion_belong_to_branch_id: str, promotion_belong_to_branch_update: PromotionBelongToBranchUpdate, db: Session = Depends(get_db)) -> Any:
    promotion_belong_to_branch_service = PromotionBelongToBranchService(db=db)
    
    logger.info("Endpoints: update_promotion_belong_to_branch called.")
    msg, promotion_belong_to_branch_response = await promotion_belong_to_branch_service.update_promotion_belong_to_branch(promotion_belong_to_branch_id, promotion_belong_to_branch_update)
    logger.info("Endpoints: update_promotion_belong_to_branch called successfully.")
    return make_response_object(promotion_belong_to_branch_response, msg)

@router.delete("/promotions_belong_to_branch/{promotion_belong_to_branch_id}")
async def delete_promotion_belong_to_branch(promotion_belong_to_branch_id: str, db: Session = Depends(get_db)) -> Any:
    promotion_belong_to_branch_service = PromotionBelongToBranchService(db=db)
    
    logger.info("Endpoints: delete_promotion_belong_to_branch called.")
    msg, promotion_belong_to_branch_response = await promotion_belong_to_branch_service.delete_promotion_belong_to_branch(promotion_belong_to_branch_id)
    logger.info("Endpoints: delete_promotion_belong_to_branch called successfully.")
    return make_response_object(promotion_belong_to_branch_response, msg)
