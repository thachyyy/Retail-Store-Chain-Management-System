
import logging
import uuid
from fastapi import HTTPException
from sqlalchemy.orm import Session
from pydantic import UUID4

from app import crud
from app.constant.app_status import AppStatus
from app.schemas.branch import BranchCreateParams, BranchCreate, BranchUpdate
from app.core.exceptions import error_exception_handler

logger = logging.getLogger(__name__)

class BranchService:
    def __init__(self, db: Session):
        self.db = db
        
    async def get_all_branches(self):
        logger.info("BranchService: get_all_branches called.")
        result = await crud.branch.get_all_branches(db=self.db)
        logger.info("BranchService: get_all_branches called successfully.")
        
        return dict(message_code=AppStatus.SUCCESS.message), dict(data=result)
    
    async def get_branch_by_id(self, branch_id: str):
        logger.info("BranchService: get_branch_by_id called.")
        result = await crud.branch.get_branch_by_id(db=self.db, branch_id=branch_id)
        logger.info("BranchService: get_branch_by_id called successfully.")
        
        return dict(message_code=AppStatus.SUCCESS.message), dict(data=result)
    
    async def gen_id(self):
        newID: str
        lastID = await crud.branch.get_last_id(self.db)
        lenID = len(str(lastID))
        if lenID >= 9:
            return str(lastID + 1)
        else:
            newID = str(lastID + 1)
            len_rest = 9 - lenID
    
            for i in range(len_rest):
                newID = '0' + newID
    
            return 'STORE' + newID
    
    async def create_branch(self, obj_in: BranchCreateParams):
        logger.info("BranchService: get_branch_by_address called.")
        current_branch_address = await crud.branch.get_branch_by_address(self.db, obj_in.address)
        logger.info("BranchService: get_branch_by_address called successfully.")
        
        logger.info("BranchService: get_branch_by_phone called.")
        current_branch_phone = await crud.branch.get_branch_by_phone(self.db, obj_in.phone_number)
        logger.info("BranchService: get_branch_by_phone called successfully.")
        
        logger.info("BranchService: get_branch_by_email called.")
        current_branch_email = await crud.branch.get_branch_by_email(self.db, obj_in.email)
        logger.info("BranchService: get_branch_by_email called successfully.")
        
        logger.info("BranchService: get_branch_by_name_detail called.")
        current_branch_name_detail = await crud.branch.get_branch_by_name_detail(self.db, obj_in.name_detail)
        logger.info("BranchService: get_branch_by_name_detail called successfully.")
        
        if current_branch_address:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_BRANCH_ADDRESS_ALREADY_EXIST)
        if current_branch_phone:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_BRANCH_PHONE_ALREADY_EXIST)
        if current_branch_email:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_BRANCH_EMAIL_ALREADY_EXIST)
        if current_branch_name_detail:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_BRANCH_EMAIL_ALREADY_EXIST)
        
        newID = await self.gen_id()
            
        branch_create = BranchCreate(
            id=newID,
            name_display=obj_in.name_display,
            name_detail=obj_in.name_detail,
            address=obj_in.address,
            district=obj_in.district,
            province=obj_in.province,
            phone_number=obj_in.phone_number,
            email=obj_in.email,
            status=obj_in.status,
            note=obj_in.note,
            manager_name=obj_in.manager_name,
            manager_id=obj_in.manager_id
            
        )
        
        logger.info("BranchService: create called.")
        result = crud.branch.create(db=self.db, obj_in=branch_create)
        logger.info("BranchService: create called successfully.")
        
        self.db.commit()
        logger.info("Service: create_branch success.")
        return dict(message_code=AppStatus.SUCCESS.message)
    
    async def update_branch(self, branch_id: str, obj_in: BranchUpdate):
        logger.info("BranchService: get_branch_by_id called.")
        isValidBranch = await crud.branch.get_branch_by_id(db=self.db, branch_id=branch_id)
        logger.info("BranchService: get_branch_by_id called successfully.")
        
        if not isValidBranch:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_BRANCH_NOT_FOUND)
        
        logger.info("BranchService: update_branch called.")
        result = await crud.branch.update_branch(db=self.db, branch_id=branch_id, branch_update=obj_in)
        logger.info("BranchService: update_branch called successfully.")
        self.db.commit()
        return dict(message_code=AppStatus.UPDATE_SUCCESSFULLY.message), dict(data=result)
        
    async def delete_branch(self, branch_id: str):
        logger.info("BranchService: get_branch_by_id called.")
        isValidBranch = await crud.branch.get_branch_by_id(db=self.db, branch_id=branch_id)
        logger.info("BranchService: get_branch_by_id called successfully.")
        
        if not isValidBranch:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_BRANCH_NOT_FOUND)
        
        logger.info("BranchService: delete_branch called.")
        result = await crud.branch.delete_branch(self.db, branch_id)
        logger.info("BranchService: delete_branch called successfully.")
        
        self.db.commit()
        return dict(message_code=AppStatus.DELETED_SUCCESSFULLY.message), dict(data=result)
    
    async def get_manager_id_by_name(self, manager_name: str):
        sql = f"SELECT id FROM public.employee WHERE full_name = '{manager_name}';"
        
        logger.info("BranchService: get_manager_id_by_name called.")
        result = await crud.branch.get_manager_id_by_name(self.db, sql)
        logger.info("BranchService: get_manager_id_by_name called. successfully")
        
        return result
    
    async def whereConditionBuilderForSearch(self, condition: str) -> str:
        conditions = list()
        conditions.append(f"id::text ilike '%{condition}%'")
        conditions.append(f"name ilike '%{condition}%'")
        conditions.append(f"address ilike '%{condition}%'")
        
        manager_id_list = self.get_manager_id_by_name(condition)
        
        for id in manager_id_list:
            conditions.append(f"manager_id ilike '%{id}%'")
            
        whereCondition = "WHERE " + ' OR '.join(conditions)
        return whereCondition
    
    async def whereConditionBuilderForFilter(self, conditions: dict) -> str:
        whereList = list()
        
        if 'manager_name_list' in conditions:
            manager_id_list = self.get_manager_id_by_name(conditions)
            for id in manager_id_list:
                whereList.append(f"manager_id = '{id}'")
        if 'status' in conditions:
            whereList.append(f"status = '{conditions['status']}'")
        if 'province' in conditions:
            whereList.append(f"province = '{conditions['province']}'")
        if 'district' in conditions:
            whereList.append(f"district = '{conditions['district']}'")
            
        whereConditions = "WHERE " + ' AND '.join(whereList)
        return whereConditions
    
    async def search_branch(self, condition: str = None):
        whereCondition = await self.whereConditionBuilderForSearch(condition)
        sql = f"SELECT * FROM public.branch {whereCondition};"
        
        logger.info("BranchService: search_branch called.")
        result = await crud.branch.search_branch(self.db, sql)
        logger.info("BranchService: search_branch called successfully.")
        
        return dict(message_code=AppStatus.SUCCESS.message), dict(data=result)
    
    async def filter_branch(
        self,
        status: str = None,
        manager_name_list: list = None,
        province: str = None,
        district: str = None
):
        conditions = dict()
        
        if status:
            status = status.upper()
            conditions['status'] = status
        if manager_name_list:
            for name in manager_name_list:
                conditions['manager_name_list'] = name
        if province:
            conditions['province'] = province
        if district:
            conditions['district'] = district
        
        whereConditions = await self.whereConditionBuilderForFilter(conditions)
        sql = f"SELECT * FROM public.branch {whereConditions};"
        
        logger.info("BranchService: filter_branch called.")
        result = await crud.branch.filter_branch(self.db, sql)
        logger.info("BranchService: filter_branch called successfully.")
        
        return dict(message_code=AppStatus.SUCCESS.message), dict(data=result)