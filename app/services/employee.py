import logging
import uuid
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.utils.response import make_response_object
from pydantic import UUID4
from datetime import date

from app import crud
from app.constant.app_status import AppStatus
from app.schemas.employee import EmployeeCreateParams, EmployeeCreate, EmployeeUpdate
from app.core.exceptions import error_exception_handler

logger = logging.getLogger(__name__)

class EmployeeService:
    def __init__(self, db: Session):
        self.db = db
        
    async def get_all_employees(self):
        logger.info("EmployeeService: get_all_employees called.")
        result = await crud.employee.get_all_employees(db=self.db)
        logger.info("EmployeeService: get_all_employees called successfully.")
        
        return dict(message_code=AppStatus.SUCCESS.message), dict(data=result)
    
    async def get_employee_by_id(self, employee_id: str):
        logger.info("EmployeeService: get_employee_by_id called.")
        result = await crud.employee.get_employee_by_id(db=self.db, employee_id=employee_id)
        logger.info("EmployeeService: get_employee_by_id called successfully.")
        
        return dict(message_code=AppStatus.SUCCESS.message), dict(data=result)
    
    async def get_employee_by_branch_name(self, branch_name: str):
        logger.info("EmployeeService: get_employee_by_branch_name called.")
        result = await crud.employee.get_employee_by_branch_name(db=self.db, branch_name=branch_name)
        logger.info("EmployeeService: get_employee_by_branch_name called successfully.")
        
        return dict(message_code=AppStatus.SUCCESS.message), dict(data=result)
    
    async def gen_id(self):
        newID: str
        lastID = await crud.employee.get_last_id(self.db)
        lenID = len(str(lastID))
        if lenID >= 9:
            return str(lastID + 1)
        else:
            newID = str(lastID + 1)
            len_rest = 9 - lenID
    
            for i in range(len_rest):
                newID = '0' + newID
    
            return 'EMP' + newID
    
    async def create_employee(self, obj_in: EmployeeCreateParams):
        logger.info("EmployeeService: get_employee_by_email called.")
        current_employee_email = await crud.employee.get_employee_by_email(self.db, obj_in.email)
        logger.info("EmployeeService: get_employee_by_email called successfully.")
        
        logger.info("EmployeeService: get_employee_by_phone called.")
        current_employee_phone = await crud.employee.get_employee_by_phone(self.db, obj_in.phone_number)
        logger.info("EmployeeService: get_employee_by_phone called successfully.")
        
        if current_employee_email:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_EMAIL_ALREADY_EXIST)
        if current_employee_phone:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_PHONE_ALREADY_EXIST)
    
        # Kiểm tra chi nhánh có quản lí hay chưa
        # if obj_in.role.value == "Quản lí chi nhánh":
             
        #     logger.info("BranchService: get_branch_by_name_detail called.")
        #     current_branch =  await crud.branch.get_branch_by_name_detail(self.db,obj_in.branch_name)
        #     logger.info("BranchService: get_branch_by_name_detail called successfully.")
        #     if current_branch.manager_id:
        #         raise HTTPException(status_code=404, detail="Chi nhánh đã có quản lí.") 
        #     update_branch_manager = await crud.branch.update_branch(self.db,current_branch.id,branch_update=current_branch.manager_id)
        
        newID = await self.gen_id()

        employee_create = EmployeeCreate(
            id=newID,
            full_name=obj_in.full_name,
            date_of_birth=obj_in.date_of_birth,
            gender=obj_in.gender,
            email=obj_in.email,
            phone_number=obj_in.phone_number,
            role=obj_in.role,
            address=obj_in.address,
            district=obj_in.district,
            province=obj_in.province,
            status=obj_in.status,
            note=obj_in.note,
            branch_name=obj_in.branch_name
        )
        
        logger.info("EmployeeService: create called.")
        result = crud.employee.create(db=self.db, obj_in=employee_create)
        logger.info("EmployeeService: create called successfully.")
        
        self.db.commit()
        logger.info("Service: create_employee success.")
        return dict(message_code=AppStatus.SUCCESS.message),employee_create
    
    async def update_employee(self, employee_id: str, obj_in: EmployeeUpdate):
        logger.info("EmployeeService: get_employee_by_id called.")
        isValidEmployee = await crud.employee.get_employee_by_id(db=self.db, employee_id=employee_id)
        logger.info("EmployeeService: get_employee_by_id called successfully.")
        
        if not isValidEmployee:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_EMPLOYEE_NOT_FOUND)
        if obj_in.role.value == "Quản lí chi nhánh":
            logger.info("BranchService: get_branch_by_name_detail called.")
            current_branch =  await crud.branch.get_branch_by_name_detail(self.db,obj_in.branch_name)
            logger.info("BranchService: get_branch_by_name_detail called successfully.")
            if current_branch.manager_id:
                raise HTTPException(status_code=404, detail="Chi nhánh đã có quản lí.") 
             
        logger.info("EmployeeService: update_employee called.")
        result = await crud.employee.update_employee(db=self.db, employee_id=employee_id, employee_update=obj_in)
        logger.info("EmployeeService: update_employee called successfully.")
        self.db.commit()
        return dict(message_code=AppStatus.UPDATE_SUCCESSFULLY.message), dict(data=result)
        
    async def delete_employee(self, employee_id: str):
        logger.info("EmployeeService: get_employee_by_id called.")
        isValidEmployee = await crud.employee.get_employee_by_id(db=self.db, employee_id=employee_id)
        logger.info("EmployeeService: get_employee_by_id called successfully.")
        
        if not isValidEmployee:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_EMPLOYEE_NOT_FOUND)
        
        logger.info("EmployeeService: delete_employee called.")
        result = await crud.employee.delete_employee(self.db, employee_id)
        logger.info("EmployeeService: delete_employee called successfully.")
        
        self.db.commit()
        return dict(message_code=AppStatus.DELETED_SUCCESSFULLY.message), dict(data=result)
    
    async def whereConditionBuilderForSearch(self, condition: str) -> str:
        conditions = list()
        conditions.append(f"role::text ilike '%{condition}%'")
        conditions.append(f"status ilike '%{condition}%'")
        conditions.append(f"branch_name ilike '%{condition}%'")
        conditions.append(f"province ilike '%{condition}%'")
        
        whereCondition = "WHERE " + ' OR '.join(conditions)
        return whereCondition
    
    async def whereConditionBuilderForFilter(self, conditions: dict) -> str:
        whereList = list()
        
        if 'role' in conditions:
            whereList.append(f"role = '{conditions['role']}'")
        if 'status' in conditions:
            whereList.append(f"status = '{conditions['status']}'")
        if 'branch_name' in conditions:
            whereList.append(f"branch_name = '{conditions['branch_name']}'")
        if 'province' in conditions:
            whereList.append(f"province = '{conditions['province']}'")
        if 'district' in conditions:
            whereList.append(f"district = '{conditions['district']}'")
            
        whereConditions = "WHERE " + ' AND '.join(whereList)
        return whereConditions
    
    async def search_employee(self, condition: str = None):
        whereCondition = await self.whereConditionBuilderForSearch(condition)
        sql = f"SELECT * FROM public.employee {whereCondition};"
        
        logger.info("EmployeeService: search_employee called.")
        result = await crud.employee.search_employee(self.db, sql)
        logger.info("EmployeeService: search_employee called successfully.")
        
        return dict(message_code=AppStatus.SUCCESS.message), dict(data=result)
    
    async def filter_employee(
        self,
        status: str = None,
        role: str = None,
        branch_name: str = None,
        province: str = None,
        district: str = None
):
        conditions = dict()
        if status:
            status = status.upper()
            conditions['status'] = status
        if role:
            role = role.lower()
            conditions['role'] = role
        if branch_name:
            conditions['branch_name'] = branch_name
        if province:
            conditions['province'] = province
        if district:
            conditions['district'] = district
        
        whereConditions = await self.whereConditionBuilderForFilter(conditions)
        sql = f"SELECT * FROM public.employee {whereConditions};"
        
        logger.info("EmployeeService: filter_employee called.")
        result = await crud.employee.filter_employee(self.db, sql)
        logger.info("EmployeeService: filter_employee called successfully.")
        
        return dict(message_code=AppStatus.SUCCESS.message), dict(data=result)