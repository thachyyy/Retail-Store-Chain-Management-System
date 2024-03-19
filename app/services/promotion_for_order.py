import logging
import uuid

from sqlalchemy.orm import Session
from pydantic import UUID4
from datetime import date

from app import crud
from app.constant.app_status import AppStatus
from app.schemas.promotion_for_order import PromotionForOrderCreateParams, PromotionForOrderCreate, PromotionForOrderUpdate
from app.core.exceptions import error_exception_handler

logger = logging.getLogger(__name__)

class PromotionForOrderService:
    def __init__(self, db: Session):
        self.db = db
        
    async def get_all_promotions_for_order(self):
        logger.info("PromotionForOrderService: get_all_promotions_for_order called.")
        result = await crud.promotion_for_order.get_all_promotions_for_order(db=self.db)
        logger.info("PromotionForOrderService: get_all_promotions_for_order called successfully.")
        
        return dict(message_code=AppStatus.SUCCESS.message), dict(data=result)
    
    async def get_promotion_for_order_by_id(self, promotion_for_order_id: str):
        logger.info("PromotionForOrderService: get_promotion_for_order_by_id called.")
        result = await crud.promotion_for_order.get_promotion_for_order_by_id(db=self.db, promotion_for_order_id=promotion_for_order_id)
        logger.info("PromotionForOrderService: get_promotion_for_order_by_id called successfully.")
        
        return dict(message_code=AppStatus.SUCCESS.message), dict(data=result)
    
    async def create_promotion_for_order(self, obj_in: PromotionForOrderCreateParams):
        logger.info("PromotionForOrderService: get_promotion_for_order_by_promotion_id called.")
        sql = f"SELECT * FROM public.promotion_for_order WHERE promotion_id = '{obj_in.promotion_id}' AND purchase_order_id = '{obj_in.purchase_order_id}';"
        current_promotion_id = await crud.promotion_for_order.get_promotion_for_order(self.db, sql)
        logger.info("PromotionForOrderService: get_promotion_for_order_by_promotion_id called successfully.")
        
        if current_promotion_id:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_PROMOTION_FOR_ORDER_ALREADY_EXIST)
        
        promotion_for_order_create = PromotionForOrderCreate(
            id=uuid.uuid4(),
            promotion_id=obj_in.promotion_id,
            purchase_order_id=obj_in.purchase_order_id
        )
        
        logger.info("PromotionForOrderService: create called.")
        result = crud.promotion_for_order.create(db=self.db, obj_in=promotion_for_order_create)
        logger.info("PromotionForOrderService: create called successfully.")
        
        self.db.commit()
        logger.info("Service: create_promotion_for_order success.")
        return dict(message_code=AppStatus.SUCCESS.message), dict(data=promotion_for_order_create)
    
    async def update_promotion_for_order(self, promotion_for_order_id: str, obj_in: PromotionForOrderUpdate):
        logger.info("PromotionForOrderService: get_promotion_for_order_by_id called.")
        isValidPromotionForOrder = await crud.promotion_for_order.get_promotion_for_order_by_id(db=self.db, promotion_for_order_id=promotion_for_order_id)
        logger.info("PromotionForOrderService: get_promotion_for_order_by_id called successfully.")
        
        if not isValidPromotionForOrder:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_PROMOTION_FOR_ORDER_NOT_FOUND)
        
        logger.info("PromotionForOrderService: update_promotion_for_order called.")
        result = await crud.promotion_for_order.update_promotion_for_order(db=self.db, promotion_for_order_id=promotion_for_order_id, promotion_for_order_update=obj_in)
        logger.info("PromotionForOrderService: update_promotion_for_order called successfully.")
        self.db.commit()
        return dict(message_code=AppStatus.UPDATE_SUCCESSFULLY.message), dict(data=result)
        
    async def delete_promotion_for_order(self, promotion_for_order_id: str):
        logger.info("PromotionForOrderService: get_promotion_for_order_by_id called.")
        isValidPromotionForOrder = await crud.promotion_for_order.get_promotion_for_order_by_id(db=self.db, promotion_for_order_id=promotion_for_order_id)
        logger.info("PromotionForOrderService: get_promotion_for_order_by_id called successfully.")
        
        if not isValidPromotionForOrder:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_PROMOTION_FOR_ORDER_NOT_FOUND)
        
        logger.info("PromotionForOrderService: delete_promotion_for_order called.")
        result = await crud.promotion_for_order.delete_promotion_for_order(self.db, promotion_for_order_id)
        logger.info("PromotionForOrderService: delete_promotion_for_order called successfully.")
        
        self.db.commit()
        return dict(message_code=AppStatus.DELETED_SUCCESSFULLY.message), dict(data=result)
    