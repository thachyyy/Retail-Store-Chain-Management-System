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
from app.schemas.promotion_for_order import PromotionForOrderCreateParams, PromotionForOrderUpdate
from app.services.promotion_for_order import PromotionForOrderService
from app.utils.response import make_response_object

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/promotions_for_order")
async def create_promotion_for_order(
    promotion_for_order_create: PromotionForOrderCreateParams,
    db: Session = Depends(get_db)
) -> Any:
    promotion_for_order_service = PromotionForOrderService(db=db)
    logger.info("Endpoints: create_promotion_for_order called.")
    
    promotion_for_order_response = await promotion_for_order_service.create_promotion_for_order(promotion_for_order_create)
    logger.info("Endpoints: create_promotion_for_order called successfully.")
    return make_response_object(promotion_for_order_response)

@router.get("/promotions_for_order")
async def get_all_promotions_for_order(db: Session = Depends(get_db)) -> Any:
    promotion_for_order_service = PromotionForOrderService(db=db)
    logger.info("Endpoints: get_all_promotions_for_order called.")
    
    msg, promotion_for_order_response = await promotion_for_order_service.get_all_promotions_for_order()
    logger.info("Endpoints: get_all_promotions_for_order called successfully.")
    return make_response_object(promotion_for_order_response, msg)

@router.get("/promotions_for_order/{promotion_for_order_id}")
async def get_promotion_for_order_by_id(promotion_for_order_id: str, db: Session = Depends(get_db)) -> Any:
    promotion_for_order_service = PromotionForOrderService(db=db)
    
    logger.info("Endpoints: get_promotion_for_order_by_id called.")  
    msg, promotion_for_order_response = await promotion_for_order_service.get_promotion_for_order_by_id(promotion_for_order_id)
    logger.info("Endpoints: get_all_promotion_for_orders called successfully.")
    return make_response_object(promotion_for_order_response, msg)
    
@router.put("/promotions_for_order/{promotion_for_order_id}")
async def update_promotion_for_order(promotion_for_order_id: str, promotion_for_order_update: PromotionForOrderUpdate, db: Session = Depends(get_db)) -> Any:
    promotion_for_order_service = PromotionForOrderService(db=db)
    
    logger.info("Endpoints: update_promotion_for_order called.")
    msg, promotion_for_order_response = await promotion_for_order_service.update_promotion_for_order(promotion_for_order_id, promotion_for_order_update)
    logger.info("Endpoints: update_promotion_for_order called successfully.")
    return make_response_object(promotion_for_order_response, msg)

@router.delete("/promotions_for_order/{promotion_for_order_id}")
async def delete_promotion_for_order(promotion_for_order_id: str, db: Session = Depends(get_db)) -> Any:
    promotion_for_order_service = PromotionForOrderService(db=db)
    
    logger.info("Endpoints: delete_promotion_for_order called.")
    msg, promotion_for_order_response = await promotion_for_order_service.delete_promotion_for_order(promotion_for_order_id)
    logger.info("Endpoints: delete_promotion_for_order called successfully.")
    return make_response_object(promotion_for_order_response, msg)
