
import logging
from typing import Optional
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
        
    async def get_all_branches(
        self,
        tenant_id: str,
        limit: Optional[int] = None,
        offset:Optional[int] = None,
        status: Optional[str] = None,
        province: Optional[str] = None,
        district: Optional[str] = None,
        query_search: Optional[str] = None
        ):
        
        conditions = dict()
        if status:
            conditions['status'] = status
        if province:
            conditions['province'] = province
        if district:
            conditions['district'] = district
       
        if conditions:
            whereConditions = await self.whereConditionBuilderForFilter(conditions, tenant_id)
            sql = f"SELECT * FROM public.branch {whereConditions};"
            
            if offset is not None and limit is not None:
                sql = f"SELECT * FROM public.branch {whereConditions} LIMIT {limit} OFFSET {offset*limit};"
                
            total = f"SELECT COUNT(*) FROM public.branch {whereConditions};"

            logger.info("BranchService: filter_branch called.")
            result, total = await crud.branch.get_branch_by_conditions(self.db, sql=sql, total=total)
            logger.info("BranchService: filter_branch called successfully.")
            total = total[0]['count']
        
        elif query_search:
            whereConditions = await self.whereConditionBuilderForSearch(query_search, tenant_id)
            
            sql = f"SELECT * FROM public.branch {whereConditions};"
            
            if limit is not None and offset is not None:
                sql = f"SELECT * FROM public.branch {whereConditions} LIMIT {limit} OFFSET {offset*limit};"
                
            
            total = f"SELECT COUNT(*) FROM public.branch {whereConditions};"

            logger.info("BranchService: filter_product called.")
            result,total= await crud.branch.get_branch_by_conditions(self.db, sql=sql,total = total)
            total = total[0]['count']
            
        else: 
            logger.info("BranchService: get_all_branches called.")
            if limit is not None and offset is not None:
                result, total = crud.branch.get_multi(db=self.db, skip=offset*limit,limit=limit, tenant_id=tenant_id)
            else: result, total = crud.branch.get_multi(db=self.db, tenant_id=tenant_id)
            logger.info("BranchService: get_all_branches called successfully.")
            
        return dict(message_code=AppStatus.SUCCESS.message,total=total),result
    
    
    async def get_branch_by_id(self, branch_id: str, tenant_id: str):
        logger.info("BranchService: get_branch_by_id called.")
        result = await crud.branch.get_branch_by_id(db=self.db, branch_id=branch_id)
        logger.info("BranchService: get_branch_by_id called successfully.")
        if not result:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_BRANCH_NOT_FOUND)
        return dict(message_code=AppStatus.SUCCESS.message), result
    
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
    
    async def create_branch(self, obj_in: BranchCreateParams, tenant_id: str):
        logger.info("BranchService: get_branch_by_name_detail called.")
        current_branch_name_detail = await crud.branch.get_branch_by_name_detail(self.db, obj_in.name_detail, tenant_id)
        logger.info("BranchService: get_branch_by_name_detail called successfully.")
        
        logger.info("BranchService: get_branch_by_address called.")
        current_branch_address = await crud.branch.get_branch_by_address(self.db, obj_in.address, tenant_id)
        logger.info("BranchService: get_branch_by_address called successfully.")
        
        logger.info("BranchService: get_branch_by_phone_number called.")
        current_branch_phone_number = await crud.branch.get_branch_by_phone_number(self.db, tenant_id, obj_in.phone_number)
        logger.info("BranchService: get_branch_by_phone_number called successfully.")
        
        logger.info("BranchService: get_branch_by_email called.")
        current_branch_email = await crud.branch.get_branch_by_email(self.db, obj_in.email, tenant_id)
        logger.info("BranchService: get_branch_by_email called successfully.")
        
        if current_branch_name_detail:            
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_BRANCH_NAME_DETAIL_ALREADY_EXIST)
        
        if current_branch_address:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_BRANCH_ADDRESS_ALREADY_EXIST)
        
        if current_branch_phone_number:
            if current_branch_phone_number.phone_number:
                raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_BRANCH_PHONE_NUMBER_ALREADY_EXIST)
             
        if current_branch_email:
            if current_branch_email.email:
                raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_BRANCH_EMAIL_ALREADY_EXIST)
        
        newID = await self.gen_id()
            
        branch_create = BranchCreate(
            id=newID,
            name_display=tenant_id,
            name_detail=obj_in.name_detail,
            address=obj_in.address,
            district=obj_in.district,
            province=obj_in.province,
            phone_number=obj_in.phone_number,
            email=obj_in.email,
            status=obj_in.status,
            note=obj_in.note,
            tenant_id=tenant_id
            # manager_name=obj_in.manager_name,
            # manager_id=obj_in.manager_id
        )
        
        logger.info("BranchService: create called.")
        result = crud.branch.create(db=self.db, obj_in=branch_create)
        logger.info("BranchService: create called successfully.")
        
        self.db.commit()
        logger.info("Service: create_branch success.")
        return dict(message_code=AppStatus.SUCCESS.message), branch_create
    
    async def update_branch(self, branch_id: str, obj_in: BranchUpdate, tenant_id: str):
        logger.info("BranchService: get_branch_by_id called.")
        isValidBranch = await crud.branch.get_branch_by_id(db=self.db, branch_id=branch_id, tenant_id=tenant_id)
        logger.info("BranchService: get_branch_by_id called successfully.")
        
        if not isValidBranch:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_BRANCH_NOT_FOUND)
            
        logger.info("BranchService: get_branch_by_name_detail called.")
        current_branch_name_detail = await crud.branch.get_branch_by_name_detail(self.db, obj_in.name_detail,tenant_id,branch_id)
        logger.info("BranchService: get_branch_by_name_detail called successfully.")
        
        logger.info("BranchService: get_branch_by_address called.")
        current_branch_address = await crud.branch.get_branch_by_address(self.db, obj_in.address,tenant_id,branch_id)
        logger.info("BranchService: get_branch_by_address called successfully.")
        
        logger.info("BranchService: get_branch_by_phone_number called.")
        current_branch_phone_number = await crud.branch.get_branch_by_phone_number(self.db,tenant_id, obj_in.phone_number,branch_id)     
        logger.info("BranchService: get_branch_by_phone_number called successfully.")
        
        logger.info("BranchService: get_branch_by_email called.")
        current_branch_email = await crud.branch.get_branch_by_email(self.db, obj_in.email,tenant_id,branch_id)
        logger.info("BranchService: get_branch_by_email called successfully.")
        
        if current_branch_name_detail:
            print("current_branch_name_detail:", current_branch_name_detail.name_detail)
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_BRANCH_NAME_DETAIL_ALREADY_EXIST)
        if current_branch_address:
            print("current_branch_address:", current_branch_address.address)
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_BRANCH_ADDRESS_ALREADY_EXIST)
        if current_branch_phone_number.phone_number:
            print("current_branch_phone_number:", current_branch_phone_number.phone_number)
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_BRANCH_PHONE_NUMBER_ALREADY_EXIST)
        if current_branch_email.email:
            print("current_branch_email:", current_branch_email.email)
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_BRANCH_EMAIL_ALREADY_EXIST)
        logger.info("BranchService: update_branch called.")
        
        branch = await crud.branch.get_branch_by_id(self.db, branch_id, tenant_id)
        if branch.manager_id != obj_in.manager_id:
            await crud.branch.change_manager(self.db, branch.manager_id, obj_in.manager_id)
        
        result = await crud.branch.update_branch(db=self.db, branch_id=branch_id, branch_update=obj_in)
        logger.info("BranchService: update_branch called successfully.")
        self.db.commit()
        obj_update = await crud.branch.get_branch_by_id(self.db, branch_id, tenant_id)
        return dict(message_code=AppStatus.UPDATE_SUCCESSFULLY.message), obj_update
        
    async def delete_branch(self, branch_id: str, tenant_id: str):
        logger.info("BranchService: get_branch_by_id called.")
        isValidBranch = await crud.branch.get_branch_by_id(db=self.db, branch_id=branch_id,tenant_id=tenant_id)
        logger.info("BranchService: get_branch_by_id called successfully.")
        
        if not isValidBranch:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_BRANCH_NOT_FOUND)
        
        logger.info("BranchService: delete_branch called.")
        result = await crud.branch.delete_branch(self.db, branch_id)
        logger.info("BranchService: delete_branch called successfully.")
        
        self.db.commit()
        return dict(message_code=AppStatus.DELETED_SUCCESSFULLY.message),isValidBranch
    
    async def get_manager_id_by_name(self, manager_name: str, tenant_id: str):
        sql = f"SELECT id FROM public.employee WHERE full_name = '{manager_name}' AND tenant_id = '{tenant_id}';"
        
        logger.info("BranchService: get_manager_id_by_name called.")
        result = await crud.branch.get_manager_id_by_name(self.db, sql)
        logger.info("BranchService: get_manager_id_by_name called. successfully")
        
        return result
    
    async def whereConditionBuilderForSearch(self, condition: str, tenant_id: str) -> str:
        conditions = list()
        conditions.append(f"id::text ilike '%{condition}%'")
        conditions.append(f"name_detail ilike '%{condition}%'")
        conditions.append(f"name_display ilike '%{condition}%'")
        conditions.append(f"address ilike '%{condition}%'")
        
        manager_id_list = await self.get_manager_id_by_name(condition)
        
        for id in manager_id_list:
            conditions.append(f"manager_id ilike '%{id}%'")
            
        whereCondition = ' OR '.join(conditions)
        whereCondition = f"WHERE ({whereCondition}) AND tenant_id = '{tenant_id}'"
        return whereCondition
    
    async def whereConditionBuilderForFilter(self, conditions: dict, tenant_id: str) -> str:
        whereList = list()
        whereList.append(f"tenant_id = '{tenant_id}'")
        
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
    
    # async def search_branch(
    #     self, 
    #     condition: str = None,
    #     limit: Optional[int] = None,
    #     offset:Optional[int] = None
    # ):
    #     whereCondition = await self.whereConditionBuilderForSearch(condition)
    #     sql = f"SELECT * FROM public.branch {whereCondition};"
        
    #     if limit is not None and offset is not None:
    #         sql = f"SELECT * FROM public.branch {whereCondition} LIMIT {limit} OFFSET {offset};"
            
    #     logger.info("BranchService: search_branch called.")
    #     result = await crud.branch.get_branch_by_conditions(self.db, sql)
    #     logger.info("BranchService: search_branch called successfully.")
        
    #     total = len(result)
    #     return dict(message_code=AppStatus.SUCCESS.message, total=total), result
    