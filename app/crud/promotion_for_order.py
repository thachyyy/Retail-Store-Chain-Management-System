import logging

from pydantic import EmailStr
from typing import Optional
from sqlalchemy.orm import Session

from app.schemas.promotion_for_order import PromotionForOrderCreate, PromotionForOrderUpdate
from app.crud.base import CRUDBase
from ..models import PromotionForOrder

logger = logging.getLogger(__name__)

class CRUDPromotionForOrder(CRUDBase[PromotionForOrder, PromotionForOrderCreate, PromotionForOrderUpdate]):
    @staticmethod
    async def get_all_promotions_for_order(db: Session) -> Optional[PromotionForOrder]:
        return db.query(PromotionForOrder).all()
    
    @staticmethod
    async def get_promotion_for_order_by_id(db: Session, promotion_for_order_id: str):
        return db.query(PromotionForOrder).filter(PromotionForOrder.id == promotion_for_order_id).first()
    
    @staticmethod
    async def get_promotion_for_order(db: Session, sql: str):
        result = db.execute(sql)
        result_as_dict = result.mappings().all()
        return result_as_dict
    
    @staticmethod
    async def get_last_id(db: Session):
        sql = "SELECT MAX(SUBSTRING(id FROM '[0-9]+')::INT) FROM promotion_for_order;"
        last_id = db.execute(sql).scalar_one_or_none()
        if last_id is None:
            return 0
        return last_id
    
    @staticmethod
    def create(db: Session, *, obj_in: PromotionForOrderCreate) -> PromotionForOrder:
        logger.info("CRUDPromotionForOrder: create called.")
        logger.debug("With: PromotionForOrderCreate - %s", obj_in.dict())

        db_obj = PromotionForOrder(**obj_in.dict())
        db.add(db_obj)
        db.flush()
        db.refresh(db_obj)
        logger.info("CRUDPromotionForOrder: create called successfully.")
        return db_obj
    
    @staticmethod
    async def update_promotion_for_order(db: Session, promotion_for_order_id: str, promotion_for_order_update: PromotionForOrderUpdate):
        update_data = promotion_for_order_update.dict(exclude_none=True)
        return db.query(PromotionForOrder).filter(PromotionForOrder.id == promotion_for_order_id).update(update_data)
    
    @staticmethod
    async def delete_promotion_for_order(db: Session, promotion_for_order_id: str):
        return db.query(PromotionForOrder).filter(PromotionForOrder.id == promotion_for_order_id).delete()
    
promotion_for_order = CRUDPromotionForOrder(PromotionForOrder)