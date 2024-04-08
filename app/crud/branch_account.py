import logging

from pydantic import EmailStr
from typing import Optional
from sqlalchemy.orm import Session

from app.schemas.branch_account import BranchAccountCreate, BranchAccountUpdate
from app.crud.base import CRUDBase
from ..models import BranchAccount

logger = logging.getLogger(__name__)

class CRUDBranchAccount(CRUDBase[BranchAccount, BranchAccountCreate, BranchAccountUpdate]):
    @staticmethod
    async def create(db: Session, *, obj_in: BranchAccountCreate) -> BranchAccount:
        logger.info("CRUDBranchAccount: create called.")
        logger.debug("With: BranchAccountCreate - %s", obj_in.dict())

        db_obj = BranchAccount(**obj_in.dict())
        db.add(db_obj)
        db.flush()
        db.refresh(db_obj)
        logger.info("CRUDBranchAccount: create called successfully.")
        return db_obj
    
    @staticmethod
    async def get_by_phone_number(db: Session, phone_number: str):
        return db.query(BranchAccount).filter(BranchAccount.phone_number == phone_number).first()
    
    @staticmethod
    async def get_all_account(db: Session):
        return db.query(BranchAccount).all()
    
    @staticmethod
    def get_branch_account_by_id(db: Session, id: str):
        return db.query(BranchAccount).filter(BranchAccount.id == id).first()
    
branch_account = CRUDBranchAccount(BranchAccount)