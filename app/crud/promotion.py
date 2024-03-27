import logging

from pydantic import EmailStr
from typing import Optional
from sqlalchemy.orm import Session

from app.schemas.promotion import PromotionCreate, PromotionUpdate
from app.crud.base import CRUDBase
from ..models import Promotion

logger = logging.getLogger(__name__)

class CRUDPromotion(CRUDBase[Promotion, PromotionCreate, PromotionUpdate]):
    @staticmethod
    async def get_all_promotions(db: Session) -> Optional[Promotion]:
        return db.query(Promotion).all()
    
    @staticmethod
    async def get_promotion_by_id(db: Session, promotion_id: str):
        return db.query(Promotion).filter(Promotion.id == promotion_id).first()
    
    @staticmethod
    async def get_promotion_by_code(db: Session, promotion_code: str) -> Optional[Promotion]:
        return db.query(Promotion).filter(Promotion.promotion_code == promotion_code).first()
    
    @staticmethod
    async def get_last_id(db: Session):
        sql = "SELECT MAX(SUBSTRING(id FROM '[0-9]+')::INT) FROM promotion;"
        last_id = db.execute(sql).scalar_one_or_none()
        if last_id is None:
            return 0
        return last_id
    
    @staticmethod
    def create(db: Session, *, obj_in: PromotionCreate) -> Promotion:
        logger.info("CRUDPromotion: create called.")
        logger.debug("With: PromotionCreate - %s", obj_in.dict())

        db_obj = Promotion(**obj_in.dict())
        db.add(db_obj)
        db.flush()
        db.refresh(db_obj)
        logger.info("CRUDPromotion: create called successfully.")
        return db_obj
    
    @staticmethod
    async def update_promotion(db: Session, promotion_id: str, promotion_update: PromotionUpdate):
        update_data = promotion_update.dict(exclude_unset=True)
        return db.query(Promotion).filter(Promotion.id == promotion_id).update(update_data)
    
    @staticmethod
    async def delete_promotion(db: Session, promotion_id: str):
        return db.query(Promotion).filter(Promotion.id == promotion_id).delete()
    
    @staticmethod
    async def search_promotion(db: Session, sql: str):        
        result = db.execute(sql)
        result_as_dict = result.mappings().all()
        return result_as_dict
    
    @staticmethod
    async def filter_promotion(db: Session, sql: str):
        result = db.execute(sql)
        result_as_dict = result.mappings().all()
        return result_as_dict
    
promotion = CRUDPromotion(Promotion)