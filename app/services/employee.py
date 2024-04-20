import logging
import uuid
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.utils.response import make_response_object
from pydantic import UUID4
from datetime import date
from typing import Optional

from app import crud
from app.constant.app_status import AppStatus
from app.schemas.employee import EmployeeCreateParams, EmployeeCreate, EmployeeUpdate
from app.core.exceptions import error_exception_handler
from app.utils import hash_lib
from app.models import Employee
from app.schemas.tenant import TenantCreate


logger = logging.getLogger(__name__)

class EmployeeService:
    def __init__(self, db: Session):
        self.db = db
        
    async def create_user(self, obj_in):
        logger.info("EmployeeService: get_info called.")
        current_email = await crud.employee.get_employee_by_email(self.db, obj_in.email.lower())
        current_tenant = await crud.tenant.get_tenant_by_id(self.db, obj_in.branch_name)
        
        if current_tenant:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_BRANCH_NAME_ALREADY_EXIST)
        
        if current_email and current_email.hashed_password:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_EMAIL_ALREADY_EXIST)
        
        if len(obj_in.password) < 6 or len(obj_in.password) > 64:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_PASSWORD_LENGTH)
        
        if obj_in.password != obj_in.password_confirm:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_PASSWORD_CONFIRM_NOT_MATCH)

        obj_in.email = obj_in.email.lower()
        new_id = await self.gen_id()
        hashed_password = hash_lib.hash_password(obj_in.password)

        user_create = EmployeeCreate(
            id=new_id,
            full_name=obj_in.full_name,
            email=obj_in.email,
            phone_number=obj_in.phone_number,
            role="Quản lý",
            status="Đang làm việc",
            hashed_password=hashed_password,
            tenant_id=obj_in.branch
        )
        result = await crud.employee.create(db=self.db, obj_in=user_create)
        
        tenant_create = TenantCreate(
            tenant_id=obj_in.branch,
            email=obj_in.email,
            full_name=obj_in.full_name,
        )
        
        result_tenant = await crud.tenant.create(db=self.db, obj_in=tenant_create)
        
        self.db.commit()
        logger.info("Service: create_user success.")
        return dict(message_code=AppStatus.SUCCESS.message), user_create
    
    async def login(self, obj_in) -> Employee:
        logger.info("EmployeeService: login called.")
        # Check if the user exist
        user = await crud.employee.get_employee_by_email(self.db, obj_in.email.lower())
        if not user:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_USER_NOT_FOUND)

        # Check if the password is valid
        if not hash_lib.verify_password(obj_in.password, user.hashed_password):
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_PASSWORD_INVALID)

        logger.info("UserService: login success.")
        return user
    
    async def read_me(self, employee_id: str, tanant_id: str):
        user = await crud.employee.get_employee_by_id(self.db, employee_id)
        return dict(message_code=AppStatus.SUCCESS.message), user
        
    async def get_all_employees(
        self,
        tenant_id: str,
        branch: Optional[str] = None,
        limit: Optional[int] = None,
        offset:Optional[int] = None, 
        role: str = None,
        status: str = None,
        province: str = None,
        district: str = None,
        gender: str = None,
        start_date: date = None,
        end_date: date = None,
        id: str = None,
        full_name: str = None,
        email: str = None,
        phone_number: str = None,
        address: str = None,
        note: str = None,
        query_search: Optional[str] = None
    ):
        conditions = dict()
        # conditions['tenant_id'] = tenant_id
        if role:
            conditions['role'] = role
        if status:
            conditions['status'] = status
        if province:
            conditions['province'] = province
        if district:
            conditions['district'] = district
        if gender:
            conditions['gender'] = gender
        if start_date:
            conditions['start_date'] = start_date
        if end_date:
            conditions['end_date'] = end_date
        if id:
            conditions['id'] = id
        if full_name:
            conditions['full_name'] = full_name
        if email:
            conditions['email'] = email
        if phone_number:
            conditions['phone_number'] = phone_number
        if address:
            conditions['address'] = address
        if note:
            conditions['note'] = note
        # if branch_name:
        #     conditions['branch_name'] = branch_name
            
        if conditions:
            whereConditions = await self.whereConditionBuilderForFilter(tenant_id, conditions, branch)
            sql = f"SELECT * FROM public.employee {whereConditions};"
            
            if offset is not None and limit is not None:
                sql = f"SELECT * FROM public.employee {whereConditions} LIMIT {limit} OFFSET {offset*limit};"

            total = f"SELECT COUNT(*) FROM public.employee {whereConditions};"
            
            logger.info("EmployeeService: filter_employee called.")
            result,total = await crud.employee.get_employee_by_conditions(self.db, sql=sql, total=total)
            total = total[0]['count']
            logger.info("EmployeeService: filter_employee called successfully.")
            
        elif query_search:
            whereConditions = await self.whereConditionBuilderForSearch(tenant_id, query_search, branch)
            
            sql = f"SELECT * FROM public.employee {whereConditions};"
            
            if limit is not None and offset is not None:
                sql = f"SELECT * FROM public.employee {whereConditions} LIMIT {limit} OFFSET {offset*limit};"
                
            
            total = f"SELECT COUNT(*) FROM public.employee {whereConditions};"

            logger.info("EmployeeService: filter_employee called.")
            result,total= await crud.customer.get_customer_by_conditions(self.db, sql=sql,total = total)
            total = total[0]['count']
            
        else: 
            logger.info("EmployeeService: get_all_employees called.")
            if limit is not None and offset is not None:
                result, total = crud.employee.get_multi(db=self.db, skip=offset*limit, limit=limit, tenant_id=tenant_id, branch=branch)
            else: 
                result, total = crud.employee.get_multi(db=self.db, tenant_id=tenant_id, branch=branch)
            logger.info("EmployeeService: get_all_employees called successfully.")

        
        return dict(message_code=AppStatus.SUCCESS.message,total=total), result
    
    async def get_employee_by_id(self, id: str, tenant_id: str, branch: str = None):
        logger.info("EmployeeService: get_employee_by_id called.")
        if branch:
            result = await crud.employee.get_employee_by_id(db=self.db, id=id, branch=branch)
        else:
            result = await crud.employee.get_employee_by_id(db=self.db, id=id)
        if not result:
                raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_EMPLOYEE_NOT_FOUND)
        logger.info("EmployeeService: get_employee_by_id called successfully.")
        
        return dict(message_code=AppStatus.SUCCESS.message), result
    
    async def get_employee_by_branch_name(self, branch_name: str):
        logger.info("EmployeeService: get_employee_by_branch_name called.")
        result = await crud.employee.get_employee_by_branch_name(db=self.db, branch_name=branch_name)
        if not result:
                raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_BRANCH_NOT_HAVE_EMPLOYEE)
        logger.info("EmployeeService: get_employee_by_branch_name called successfully.")
        
        return dict(message_code=AppStatus.SUCCESS.message), result
    
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
    
    async def create_employee(self, tenant_id: str, obj_in: EmployeeCreateParams):
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
        
        newID = await self.gen_id() # gen id for employee
        
        # Kiểm tra chi nhánh có quản lý hay chưa
        if obj_in.role.value == "Quản lý chi nhánh":
            logger.info("BranchService: get_branch_by_name_detail called.")
            current_branch =  await crud.branch.get_branch_by_name_detail(self.db,obj_in.branch, tenant_id)
            logger.info("BranchService: get_branch_by_name_detail called successfully.")
            if current_branch:
                if current_branch.manager_id:
                    raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_EXIST_MANAGER_ERROR)
            else:
                await crud.branch.update_manager(self.db, tenant_id, obj_in.branch, newID)
        
        if len(obj_in.password) < 6 or len(obj_in.password) > 64:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_PASSWORD_LENGTH)
        
        obj_in.email = obj_in.email.lower()
        hashed_password = hash_lib.hash_password(obj_in.password)

        employee_create = EmployeeCreate(
            id=newID,
            full_name=obj_in.full_name,
            date_of_birth=obj_in.date_of_birth,
            gender=obj_in.gender,
            email=obj_in.email,
            phone_number=obj_in.phone_number,
            hashed_password=hashed_password,
            role=obj_in.role,
            address=obj_in.address,
            district=obj_in.district,
            province=obj_in.province,
            status=obj_in.status,
            branch=obj_in.branch,
            note=obj_in.note,
            tenant_id=tenant_id
        )
        
        logger.info("EmployeeService: create called.")
        result = await crud.employee.create(db=self.db, obj_in=employee_create)
        logger.info("EmployeeService: create called successfully.")
        
        self.db.commit()
        logger.info("Service: create_employee success.")
        return dict(message_code=AppStatus.SUCCESS.message), employee_create
    
    async def update_employee(self, employee_id: str, obj_in: EmployeeUpdate, branch: str = None):
        logger.info("EmployeeService: get_employee_by_id called.")
        isValidEmployee = await crud.employee.get_employee_by_id(db=self.db, id=employee_id, branch=branch)
        logger.info("EmployeeService: get_employee_by_id called successfully.")
        
        if not isValidEmployee:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_EMPLOYEE_NOT_FOUND)
        
        # if obj_in.role is not None and obj_in.role.value == "Quản lí chi nhánh":
        #     logger.info("BranchService: get_branch_by_name_detail called.")
        #     current_branch =  await crud.branch.get_branch_by_name_detail(self.db,obj_in.branch_name)
        #     logger.info("BranchService: get_branch_by_name_detail called successfully.")
        #     if current_branch.manager_id:
        #         raise HTTPException(status_code=404, detail="Chi nhánh đã có quản lí.")
            
        if obj_in.phone_number:
            isExistPhoneNumber = await crud.employee.get_employee_by_phone(self.db, obj_in.phone_number, employee_id)
            if isExistPhoneNumber:
                raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_PHONE_ALREADY_EXIST)
        
        if obj_in.email:
            isExistEmail = await crud.employee.get_employee_by_email(self.db, obj_in.email, employee_id)
            if isExistEmail:
                raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_EMAIL_ALREADY_EXIST)
            obj_in.email = obj_in.email.lower()
             
        logger.info("EmployeeService: update_employee called.")
        result = await crud.employee.update_employee(db=self.db, employee_id=employee_id, employee_update=obj_in)
        logger.info("EmployeeService: update_employee called successfully.")
        self.db.commit()
        obj_update = await crud.employee.get_employee_by_id(self.db, employee_id, branch=branch)
        return dict(message_code=AppStatus.UPDATE_SUCCESSFULLY.message), obj_update
        
    async def delete_employee(self, id: str, branch: str = None):
        logger.info("EmployeeService: get_employee_by_id called.")
        isValidEmployee = await crud.employee.get_employee_by_id(db=self.db, id=id, branch=branch)
        logger.info("EmployeeService: get_employee_by_id called successfully.")
        
        if not isValidEmployee:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_EMPLOYEE_NOT_FOUND)
        
        obj_del = await crud.employee.get_employee_by_id(self.db, id, branch)
        
        logger.info("EmployeeService: delete_employee called.")
        result = await crud.employee.delete_employee(self.db, id)
        logger.info("EmployeeService: delete_employee called successfully.")
        
        self.db.commit()
        return dict(message_code=AppStatus.DELETED_SUCCESSFULLY.message), obj_del
    
    async def whereConditionBuilderForSearch(self, tenant_id: str, condition: str, branch: str = None) -> str:
        conditions = list()
        conditions.append(f"id::text ilike '%{condition}%'")
        conditions.append(f"full_name::text ilike '%{condition}%'")
        # conditions.append(f"phone_number ilike '%{condition}%'")
        # conditions.append(f"address ilike '%{condition}%'")
        # conditions.append(f"district ilike '%{condition}%'")
        # conditions.append(f"province ilike '%{condition}%'")
        
        whereCondition = ' OR '.join(conditions)
        if branch is not None:
            whereCondition = f"WHERE ({whereCondition}) AND tenant_id = '{tenant_id}' AND = '{branch}'"
        else:
            whereCondition = f"WHERE ({whereCondition}) AND tenant_id = '{tenant_id}'"
        return whereCondition
    
    async def whereConditionBuilderForFilter(self, tenant_id: str, conditions: dict, branch: str = None) -> str:
        whereList = list()
        whereList.append(f"tenant_id = '{tenant_id}'")
        if branch is not None:
            whereList.append(f"branch = '{branch}'")
        
        # filter using '='
        if 'role' in conditions:
            whereList.append(f"role = '{conditions['role']}'")
        if 'status' in conditions:
            whereList.append(f"status = '{conditions['status']}'")
        if 'province' in conditions:
            whereList.append(f"province = '{conditions['province']}'")
        if 'district' in conditions:
            whereList.append(f"district = '{conditions['district']}'")
        if 'gender' in conditions:
            whereList.append(f"gender = '{conditions['gender']}'")
        if 'start_date' in conditions and 'end_date' in conditions:
            whereList.append(f"date_of_birth BETWEEN '{conditions['start_date']}' AND '{conditions['end_date']}'")
        
        # filter using 'ilike'
        if 'id' in conditions:
            whereList.append(f"id ilike '%{conditions['id']}%'")
        if 'full_name' in conditions:
            whereList.append(f"full_name ilike '%{conditions['full_name']}%'")
        if 'email' in conditions:
            whereList.append(f"email ilike '%{conditions['email']}%'")
        if 'phone_number' in conditions:
            whereList.append(f"phone_number ilike '%{conditions['phone_number']}%'")
        if 'address' in conditions:
            whereList.append(f"address ilike '%{conditions['address']}%'")
        if 'note' in conditions:
            whereList.append(f"note ilike '%{conditions['note']}%'")
        if 'branch' in conditions:
            whereList.append(f"branch_name ilike '%{conditions['branch']}%'")
            
        whereConditions = "WHERE " + ' AND '.join(whereList)
        return whereConditions
    
    # async def search_employee(
    #     self, 
    #     condition: str = None,
    #     limit: Optional[int] = None,
    #     offset:Optional[int] = None
    # ):
    #     whereCondition = await self.whereConditionBuilderForSearch(condition)
    #     sql = f"SELECT * FROM public.employee {whereCondition};"
        
    #     if limit is not None and offset is not None:
    #         sql = f"SELECT * FROM public.employee {whereCondition} LIMIT {limit} OFFSET {offset};"
            
    #     logger.info("EmployeeService: search_employee called.")
    #     result = await crud.employee.get_employee_by_conditions(self.db, sql)
    #     logger.info("EmployeeService: search_employee called successfully.")
        
    #     total = len(result)
    #     return dict(message_code=AppStatus.SUCCESS.message, total=total), result
    
#     async def filter_employee(
#         self,
#         status: str = None,
#         role: str = None,
#         branch_name: str = None,
#         province: str = None,
#         district: str = None
# ):
#         conditions = dict()
#         if status:
#             status = status.upper()
#             conditions['status'] = status
#         if role:
#             role = role.lower()
#             conditions['role'] = role
#         if branch_name:
#             conditions['branch_name'] = branch_name
#         if province:
#             conditions['province'] = province
#         if district:
#             conditions['district'] = district
        
#         whereConditions = await self.whereConditionBuilderForFilter(conditions)
#         sql = f"SELECT * FROM public.employee {whereConditions};"
        
#         logger.info("EmployeeService: filter_employee called.")
#         result = await crud.employee.filter_employee(self.db, sql)
#         logger.info("EmployeeService: filter_employee called successfully.")
        
#         return dict(message_code=AppStatus.SUCCESS.message), dict(data=result)