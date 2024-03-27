import logging

from pydantic import EmailStr
from typing import Optional
from sqlalchemy.orm import Session

from app.schemas.promotion_belong_to_branch import PromotionBelongToBranchCreate, PromotionBelongToBranchUpdate
from app.crud.base import CRUDBase
from ..models import PromotionBelongToBranch

logger = logging.getLogger(__name__)

class CRUDPromotionBelongToBranch(CRUDBase[PromotionBelongToBranch, PromotionBelongToBranchCreate, PromotionBelongToBranchUpdate]):
    @staticmethod
    async def get_all_promotions_belong_to_branch(db: Session) -> Optional[PromotionBelongToBranch]:
        return db.query(PromotionBelongToBranch).all()
    
    @staticmethod
    async def get_promotion_belong_to_branch_by_id(db: Session, promotion_belong_to_branch_id: str):
        return db.query(PromotionBelongToBranch).filter(PromotionBelongToBranch.id == promotion_belong_to_branch_id).first()
    
    @staticmethod
    async def get_promotion_belong_to_branch_by_promotion_id(db: Session, promotion_id: str):
        return db.query(PromotionBelongToBranch).filter(PromotionBelongToBranch.promotion_id == promotion_id).first()
    
    @staticmethod
    async def get_last_id(db: Session):
        sql = "SELECT MAX(SUBSTRING(id FROM '[0-9]+')::INT) FROM promotion_belong_to_branch;"
        last_id = db.execute(sql).scalar_one_or_none()
        if last_id is None:
            return 0
        return last_id
    
    @staticmethod
    def create(db: Session, *, obj_in: PromotionBelongToBranchCreate) -> PromotionBelongToBranch:
        logger.info("CRUDPromotionBelongToBranch: create called.")
        logger.debug("With: PromotionBelongToBranchCreate - %s", obj_in.dict())

        db_obj = PromotionBelongToBranch(**obj_in.dict())
        db.add(db_obj)
        db.flush()
        db.refresh(db_obj)
        logger.info("CRUDPromotionBelongToBranch: create called successfully.")
        return db_obj
    
    @staticmethod
    async def update_promotion_belong_to_branch(db: Session, promotion_belong_to_branch_id: str, promotion_belong_to_branch_update: PromotionBelongToBranchUpdate):
        update_data = promotion_belong_to_branch_update.dict(exclude_unset=True)
        return db.query(PromotionBelongToBranch).filter(PromotionBelongToBranch.id == promotion_belong_to_branch_id).update(update_data)
    
    @staticmethod
    async def delete_promotion_belong_to_branch(db: Session, promotion_belong_to_branch_id: str):
        return db.query(PromotionBelongToBranch).filter(PromotionBelongToBranch.id == promotion_belong_to_branch_id).delete()
    
promotion_belong_to_branch = CRUDPromotionBelongToBranch(PromotionBelongToBranch)