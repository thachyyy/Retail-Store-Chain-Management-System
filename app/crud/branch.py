import logging

from typing import Optional
from sqlalchemy import null
from sqlalchemy.orm import Session
from pydantic import UUID4

from app.schemas.branch import BranchCreate, BranchUpdate
from app.crud.base import CRUDBase
from ..models import Branch

from app.core.exceptions import error_exception_handler
from app.constant.app_status import AppStatus

logger = logging.getLogger(__name__)

class CRUDBranch(CRUDBase[Branch, BranchCreate, BranchUpdate]):
    @staticmethod
    async def get_all_branches(db: Session, offset: int = None, limit: int = None) -> Optional[Branch]:
        result = db.query(Branch)
        
        if offset is not None and limit is not None:
            result = result.offset(offset).limit(limit)
        
        return result.all()
    
    @staticmethod
    async def get_branch_by_id(db: Session, branch_id: str, tenant_id: str):
        return db.query(Branch).filter(Branch.id == branch_id, Branch.tenant_id == tenant_id).first()
    
    @staticmethod
    async def get_branch_by_address(db: Session, address: str, tenant_id: str, id: str = None) -> Optional[Branch]:
        if id:
            return db.query(Branch).filter(Branch.address == address,Branch.id != id, Branch.tenant_id == tenant_id).first()
        return db.query(Branch).filter(Branch.address == address, Branch.tenant_id == tenant_id).first()
    
    @staticmethod
    async def get_branch_by_phone_number(db: Session, tenant_id: str, phone_number: str, id: str = None) -> Optional[Branch]:
        if id:
            return db.query(Branch).filter(Branch.phone_number == phone_number,Branch.id != id, Branch.tenant_id == tenant_id).first()
        return db.query(Branch).filter(Branch.phone_number == phone_number, Branch.tenant_id == tenant_id).first()

    
    @staticmethod
    async def get_branch_by_email(db: Session, email: str, tenant_id: str, id: str= None) -> Optional[Branch]:
        if id:
            return db.query(Branch).filter(Branch.email == email,Branch.id != id, Branch.tenant_id == tenant_id).first()
        return db.query(Branch).filter(Branch.email == email, Branch.tenant_id == tenant_id).first()
    
    @staticmethod
    async def get_branch_by_name_detail(db: Session, name_detail: str, tenant_id: str, id: str = None) -> Optional[Branch]:
        if id:
            return db.query(Branch).filter(Branch.name_detail == name_detail,Branch.id != id, Branch.tenant_id == tenant_id).first()
        return db.query(Branch).filter(Branch.name_detail == name_detail, Branch.tenant_id == tenant_id).first()
    
    @staticmethod
    async def get_manager_id_by_name(db: Session, sql: str):
        result = db.execute(sql)
        result_as_dict = result.mappings().all()
        return result_as_dict
    
    @staticmethod
    async def get_branch_by_manager_id(db: Session, tenant_id: str, manager_id: str) -> Optional[Branch]:
        return db.query(Branch).filter(Branch.manager_id == manager_id, Branch.tenant_id == tenant_id).first()
    
    @staticmethod
    async def change_manager(db: Session, old_manager: str, new_manager: str):
        sql = f"""
            UPDATE public.employee SET role = 'Nhân viên' WHERE id = '{old_manager}';
            UPDATE public.employee SET role = 'Quản lý cửa hàng' WHERE id = '{new_manager}';
        """
        result = db.execute(sql)
        return result
        
        
    @staticmethod
    async def get_last_id(db: Session):
        sql = "SELECT MAX(SUBSTRING(id FROM '[0-9]+')::INT) FROM branch;"
        last_id = db.execute(sql).scalar_one_or_none()
        if last_id is None:
            return 0
        return last_id
    
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
    async def update_manager(db: Session, tenant_id: str, name_detail: str, manager_id: str):
        sql = f"UPDATE public.branch SET manager_id = '{manager_id}' WHERE name_detail = '{name_detail}' AND tenant_id = '{tenant_id}';"
        result = db.execute(sql)
        return result
    
    @staticmethod
    async def delete_branch(db: Session, branch_id: str):
        try:
            return db.query(Branch).filter(Branch.id == branch_id).delete()
        except:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_DATA_USED_ERROR)
    
    @staticmethod
    async def get_branch_by_conditions(db: Session, sql: str, total: str):        
        result = db.execute(sql)
        sum = db.execute(total)
        sum = sum.mappings().all()
        result_as_dict = result.mappings().all()
        return result_as_dict, sum
    
branch = CRUDBranch(Branch)