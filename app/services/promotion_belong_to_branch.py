import logging
import uuid

from sqlalchemy.orm import Session
from pydantic import UUID4
from datetime import date

from app import crud
from app.constant.app_status import AppStatus
from app.schemas.promotion_belong_to_branch import PromotionBelongToBranchCreateParams, PromotionBelongToBranchCreate, PromotionBelongToBranchUpdate
from app.core.exceptions import error_exception_handler

logger = logging.getLogger(__name__)

class PromotionBelongToBranchService:
    def __init__(self, db: Session):
        self.db = db
        
    async def get_all_promotions_belong_to_branch(self):
        logger.info("PromotionBelongToBranchService: get_all_promotions_belong_to_branch called.")
        result = await crud.promotion_belong_to_branch.get_all_promotions_belong_to_branch(db=self.db)
        logger.info("PromotionBelongToBranchService: get_all_promotions_belong_to_branch called successfully.")
        
        return dict(message_code=AppStatus.SUCCESS.message), dict(data=result)
    
    async def get_promotion_belong_to_branch_by_id(self, promotion_belong_to_branch_id: str):
        logger.info("PromotionBelongToBranchService: get_promotion_belong_to_branch_by_id called.")
        result = await crud.promotion_belong_to_branch.get_promotion_belong_to_branch_by_id(db=self.db, promotion_belong_to_branch_id=promotion_belong_to_branch_id)
        logger.info("PromotionBelongToBranchService: get_promotion_belong_to_branch_by_id called successfully.")
        
        return dict(message_code=AppStatus.SUCCESS.message), dict(data=result)
    
    async def create_promotion_belong_to_branch(self, obj_in: PromotionBelongToBranchCreateParams):
        logger.info("PromotionBelongToBranchService: get_promotion_belong_to_branch_by_promotion_id called.")
        current_promotion_id = await crud.promotion_belong_to_branch.get_promotion_belong_to_branch_by_promotion_id(self.db, obj_in.prmotion_id)
        logger.info("PromotionBelongToBranchService: get_promotion_belong_to_branch_by_promotion_id called successfully.")
        
        if current_promotion_id:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_PROMOTION_ID_ALREADY_EXIST)
        
        promotion_belong_to_branch_create = PromotionBelongToBranchCreate(
            id=uuid.uuid4(),
            promotion_id=obj_in.promotion_id,
            branch_id=obj_in.branch_id
        )
        
        logger.info("PromotionBelongToBranchService: create called.")
        result = crud.promotion_belong_to_branch.create(db=self.db, obj_in=promotion_belong_to_branch_create)
        logger.info("PromotionBelongToBranchService: create called successfully.")
        
        self.db.commit()
        logger.info("Service: create_promotion_belong_to_branch success.")
        return dict(message_code=AppStatus.SUCCESS.message), dict(data=promotion_belong_to_branch_create)
    
    async def update_promotion_belong_to_branch(self, promotion_belong_to_branch_id: str, obj_in: PromotionBelongToBranchUpdate):
        logger.info("PromotionBelongToBranchService: get_promotion_belong_to_branch_by_id called.")
        isValidPromotionBelongToBranch = await crud.promotion_belong_to_branch.get_promotion_belong_to_branch_by_id(db=self.db, promotion_belong_to_branch_id=promotion_belong_to_branch_id)
        logger.info("PromotionBelongToBranchService: get_promotion_belong_to_branch_by_id called successfully.")
        
        if not isValidPromotionBelongToBranch:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_PROMOTION_BELONG_TO_BRANCH_NOT_FOUND)
        
        logger.info("PromotionBelongToBranchService: update_promotion_belong_to_branch called.")
        result = await crud.promotion_belong_to_branch.update_promotion_belong_to_branch(db=self.db, promotion_belong_to_branch_id=promotion_belong_to_branch_id, promotion_belong_to_branch_update=obj_in)
        logger.info("PromotionBelongToBranchService: update_promotion_belong_to_branch called successfully.")
        self.db.commit()
        return dict(message_code=AppStatus.UPDATE_SUCCESSFULLY.message), dict(data=result)
        
    async def delete_promotion_belong_to_branch(self, promotion_belong_to_branch_id: str):
        logger.info("PromotionBelongToBranchService: get_promotion_belong_to_branch_by_id called.")
        isValidPromotionBelongToBranch = await crud.promotion_belong_to_branch.get_promotion_belong_to_branch_by_id(db=self.db, promotion_belong_to_branch_id=promotion_belong_to_branch_id)
        logger.info("PromotionBelongToBranchService: get_promotion_belong_to_branch_by_id called successfully.")
        
        if not isValidPromotionBelongToBranch:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_PROMOTION_BELONG_TO_BRANCH_NOT_FOUND)
        
        logger.info("PromotionBelongToBranchService: delete_promotion_belong_to_branch called.")
        result = await crud.promotion_belong_to_branch.delete_promotion_belong_to_branch(self.db, promotion_belong_to_branch_id)
        logger.info("PromotionBelongToBranchService: delete_promotion_belong_to_branch called successfully.")
        
        self.db.commit()
        return dict(message_code=AppStatus.DELETED_SUCCESSFULLY.message), dict(data=result)
    