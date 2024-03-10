import logging

from typing import Optional
from sqlalchemy.orm import Session
from pydantic import UUID4

from app.schemas.branch import BranchCreate, BranchUpdate
from app.crud.base import CRUDBase
from ..models import Branch

logger = logging.getLogger(__name__)

class CRUDBranch(CRUDBase[Branch, BranchCreate, BranchUpdate]):
    @staticmethod
    async def get_all_branches(db: Session) -> Optional[Branch]:
        return db.query(Branch).all()
    
    @staticmethod
    async def get_branch_by_id(db: Session, branch_id: str):
        return db.query(Branch).filter(Branch.id == branch_id).first()
    
    @staticmethod
    async def get_branch_by_address(db: Session, address: str) -> Optional[Branch]:
        return db.query(Branch).filter(Branch.address == address).first()
    
    @staticmethod
    async def get_branch_by_phone(db: Session, phone_number: str) -> Optional[Branch]:
        return db.query(Branch).filter(Branch.phone_number == phone_number).first()
    
    @staticmethod
    async def get_branch_by_email(db: Session, email: str) -> Optional[Branch]:
        return db.query(Branch).filter(Branch.email == email).first()
    
    @staticmethod
    async def get_branch_by_name_detail(db: Session, name_detail: str) -> Optional[Branch]:
        return db.query(Branch).filter(Branch.name_detail == name_detail).first()
    
    @staticmethod
    async def get_manager_id_by_name(db: Session, sql: str):
        result = db.execute(sql)
        result_as_dict = result.mappings().all()
        return result_as_dict
    
    @staticmethod
    def create(db: Session, *, obj_in: BranchCreate) -> Branch:
        logger.info("CRUDBranch: create called.")
        logger.debug("With: BranchCreate - %s", obj_in.dict())

        db_obj = Branch(**obj_in.dict())
        db.add(db_obj)
        db.flush()
        db.refresh(db_obj)
        logger.info("CRUDBranch: create called successfully.")
        return db_obj
 
    @staticmethod
    async def update_branch(db: Session, branch_id: str, branch_update: BranchUpdate):
        update_data = branch_update.dict(exclude_none=True)
        return db.query(Branch).filter(Branch.id == branch_id).update(update_data)
    
    @staticmethod
    async def delete_branch(db: Session, branch_id: str):
        return db.query(Branch).filter(Branch.id == branch_id).delete()
    
    @staticmethod
    async def search_branch(db: Session, sql: str):        
        result = db.execute(sql)
        result_as_dict = result.mappings().all()
        return result_as_dict
    
    @staticmethod
    async def filter_branch(db: Session, sql: str):
        result = db.execute(sql)
        result_as_dict = result.mappings().all()
        return result_as_dict
    
branch = CRUDBranch(Branch)