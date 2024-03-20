import logging
import uuid

from sqlalchemy.orm import Session
from pydantic import UUID4
from datetime import date

from app import crud
from app.constant.app_status import AppStatus
from app.schemas.promotion import PromotionCreateParams, PromotionCreate, PromotionUpdate
from app.core.exceptions import error_exception_handler

logger = logging.getLogger(__name__)

class PromotionService:
    def __init__(self, db: Session):
        self.db = db
        
    async def get_all_promotions(self):
        logger.info("PromotionService: get_all_promotions called.")
        result = await crud.promotion.get_all_promotions(db=self.db)
        logger.info("PromotionService: get_all_promotions called successfully.")
        
        return dict(message_code=AppStatus.SUCCESS.message), dict(data=result)
    
    async def get_promotion_by_id(self, promotion_id: str):
        logger.info("PromotionService: get_promotion_by_id called.")
        result = await crud.promotion.get_promotion_by_id(db=self.db, promotion_id=promotion_id)
        logger.info("PromotionService: get_promotion_by_id called successfully.")
        
        return dict(message_code=AppStatus.SUCCESS.message), dict(data=result)
    
    async def gen_id(self):
        newID: str
        lastID = await crud.promotion.get_last_id(self.db)
        lenID = len(str(lastID))
        if lenID >= 9:
            return str(lastID + 1)
        else:
            newID = str(lastID + 1)
            len_rest = 9 - lenID
    
            for i in range(len_rest):
                newID = '0' + newID
    
            return 'PROMO' + newID
    
    async def create_promotion(self, obj_in: PromotionCreateParams):
        logger.info("PromotionService: get_promotion_by_code called.")
        current_promotion_code = await crud.promotion.get_promotion_by_code(self.db, obj_in.promotion_code)
        logger.info("PromotionService: get_promotion_by_code called successfully.")
        
        if current_promotion_code:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_PROMOTION_CODE_ALREADY_EXIST)
        
        newID = await self.gen_id()
        
        promotion_create = PromotionCreate(
            id=newID,
            promotion_code=obj_in.promotion_code,
            promotion_name=obj_in.promotion_name,
            promotion_type=obj_in.promotion_type,
            promotion_value=obj_in.promotion_value,
            max_discount_amount=obj_in.max_discount_amount,
            start_date=obj_in.start_date,
            end_date=obj_in.end_date,
            status=obj_in.status,
            min_product_value=obj_in.min_product_value,
            min_product_quantity=obj_in.min_product_quantity
        )
        
        logger.info("PromotionService: create called.")
        result = crud.promotion.create(db=self.db, obj_in=promotion_create)
        logger.info("PromotionService: create called successfully.")
        
        self.db.commit()
        logger.info("Service: create_promotion success.")
        return dict(message_code=AppStatus.SUCCESS.message)
    
    async def update_promotion(self, promotion_id: str, obj_in: PromotionUpdate):
        logger.info("PromotionService: get_promotion_by_id called.")
        isValidPromotion = await crud.promotion.get_promotion_by_id(db=self.db, promotion_id=promotion_id)
        logger.info("PromotionService: get_promotion_by_id called successfully.")
        
        if not isValidPromotion:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_PROMOTION_NOT_FOUND)
        
        logger.info("PromotionService: update_promotion called.")
        result = await crud.promotion.update_promotion(db=self.db, promotion_id=promotion_id, promotion_update=obj_in)
        logger.info("PromotionService: update_promotion called successfully.")
        self.db.commit()
        return dict(message_code=AppStatus.UPDATE_SUCCESSFULLY.message), dict(data=result)
        
    async def delete_promotion(self, promotion_id: str):
        logger.info("PromotionService: get_promotion_by_id called.")
        isValidPromotion = await crud.promotion.get_promotion_by_id(db=self.db, promotion_id=promotion_id)
        logger.info("PromotionService: get_promotion_by_id called successfully.")
        
        if not isValidPromotion:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_PROMOTION_NOT_FOUND)
        
        logger.info("PromotionService: delete_promotion called.")
        result = await crud.promotion.delete_promotion(self.db, promotion_id)
        logger.info("PromotionService: delete_promotion called successfully.")
        
        self.db.commit()
        return dict(message_code=AppStatus.DELETED_SUCCESSFULLY.message), dict(data=result)
    
    async def whereConditionBuilderForSearch(self, condition: str) -> str:
        conditions = list()
        conditions.append(f"id::text ilike '%{condition}%'")
        conditions.append(f"promotion_name ilike '%{condition}%'")
        conditions.append(f"promotion_code ilike '%{condition}%'")
            
        whereCondition = "WHERE " + ' OR '.join(conditions)
        return whereCondition
    
    async def whereConditionBuilderForFilter(self, conditions: dict) -> str:
        whereList = list()
        
        if 'status' in conditions:
            whereList.append(f"status = '{conditions['status']}'")
            
        whereConditions = "WHERE " + ' AND '.join(whereList)
        return whereConditions
    
    async def search_promotion(self, condition: str = None):
        whereCondition = await self.whereConditionBuilderForSearch(condition)
        sql = f"SELECT * FROM public.promotion {whereCondition};"
        
        logger.info("PromotionService: search_promotion called.")
        result = await crud.promotion.search_promotion(self.db, sql)
        logger.info("PromotionService: search_promotion called successfully.")
        
        return dict(message_code=AppStatus.SUCCESS.message), dict(data=result)
    
    async def filter_promotion(
        self,
        status: str = None,
):
        conditions = dict()
        if status:
            status = status.upper()
            conditions['status'] = status
        
        whereConditions = await self.whereConditionBuilderForFilter(conditions)
        sql = f"SELECT * FROM public.promotion {whereConditions};"
        
        logger.info("PromotionService: filter_promotion called.")
        result = await crud.promotion.filter_promotion(self.db, sql)
        logger.info("PromotionService: filter_promotion called successfully.")
        
        return dict(message_code=AppStatus.SUCCESS.message), dict(data=result)