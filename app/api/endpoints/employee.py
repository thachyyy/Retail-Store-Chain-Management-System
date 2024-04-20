import logging

from typing import Any, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from pydantic import UUID4
from datetime import date

from app.api.depends import oauth2
from app.api.depends.oauth2 import create_access_token, create_refresh_token, verify_refresh_token
from app.constant.app_status import AppStatus
from app.core.exceptions import error_exception_handler
from app.db.database import get_db
from app.schemas.employee import EmployeeCreateParams, EmployeeUpdate, EmployeeRegister, EmployeeLogin
from app.services.employee import EmployeeService
from app.utils.response import make_response_object
from app.models import Employee

logger = logging.getLogger(__name__)
router = APIRouter()




@router.post('/auth/register')
async def create_user(
        employee_create: EmployeeRegister,
        db: Session = Depends(get_db)
) -> Any:
    """
    Create user.
    """
    employee_service = EmployeeService(db=db)
    logger.info("Endpoints: create_user called.")

    msg, emp_response = await employee_service.create_user(employee_create)
    logger.info("Endpoints: create_user called successfully.")
    return make_response_object(emp_response, msg)

@router.post("/auth/login")
async def login(
        login_request: EmployeeLogin,
        db: Session = Depends(get_db),
) -> Any:
    """
    login social.
    """
    logger.info("Service: login called.")

    employee_service = EmployeeService(db=db)
    current_user = await employee_service.login(login_request)

    created_access_token = create_access_token(data={"uid": current_user.id, 
                                                     "tenant_id": current_user.tenant_id,
                                                     "branch": current_user.branch,
                                                     "role": current_user.role})
    created_refresh_token = create_refresh_token(data={"uid": current_user.id, 
                                                       "tenant_id": current_user.tenant_id,
                                                       "branch": current_user.branch,
                                                       "role": current_user.role})
    logger.info("Service: read_user_me successfully.")
    return make_response_object(data=dict(access_token=created_access_token,
                                          refresh_token=created_refresh_token),
                                meta=AppStatus.LOGIN_SUCCESS.meta)

@router.post("/auth/refresh")
async def refresh_token(decoded_refresh_token=Depends(verify_refresh_token),
                        db: Session = Depends(get_db)):
    logger.info("Service: refresh_token called.")
    employee_service = EmployeeService(db=db)
    msg, current_user = await employee_service.get_employee_by_id(decoded_refresh_token['uid'])
    
    if not current_user:
        raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_USER_NOT_FOUND)

    created_access_token = create_access_token(data={"uid": current_user.id, 
                                                     "tenant_id": current_user.tenant_id,
                                                     "branch": current_user.branch,
                                                     "role": current_user.role})
    created_refresh_token = create_refresh_token(data={"uid": current_user.id, 
                                                       "tenant_id": current_user.tenant_id,
                                                       "branch": current_user.branch,
                                                       "role": current_user.role})
    logger.info("Service: refresh_token called successfully.")
    return make_response_object(data=dict(access_token=created_access_token,
                                          refresh_token=created_refresh_token),meta=msg)

@router.get("/read_me")
async def read_me(
    user: Employee = Depends(oauth2.get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    current_user = await user
    employee_service = EmployeeService(db=db)
    
    msg, user = await employee_service.read_me(current_user.id, current_user.tenant_id)
    
    return make_response_object(user, msg)
    

@router.post("/employees")
async def create_employee(
    employee_create: EmployeeCreateParams,
    user: Employee = Depends(oauth2.get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    current_user = await user
    
    if current_user.role == "Nhân viên":
        raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_ACCESS_DENIED)
    if current_user.role == "Quản lý chi nhánh":
        if employee_create.role == "Quản lý" or employee_create.role == "Quản lý chi nhánh":
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_ACCESS_DENIED)
    
    
    employee_service = EmployeeService(db=db)
    logger.info("Endpoints: create_employee called.")
    
    msg,employee_response = await employee_service.create_employee(current_user.tenant_id, employee_create)
    logger.info("Endpoints: create_employee called successfully.")
    return make_response_object(employee_response,msg)

@router.get("/employees")
async def get_all_employees(
    user: Employee = Depends(oauth2.get_current_user),
    branch: Optional[str] = None,
    db: Session = Depends(get_db),
    limit: int = None,
    offset: int = None,
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
    query_search: Optional[str] = None,
    
) -> Any:
    
    current_user = await user
    
    if current_user.role == "Nhân viên":
        raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_ACCESS_DENIED)
    
    branch = current_user.branch
    
    employee_service = EmployeeService(db=db)
    logger.info("Endpoints: get_all_employees called.")
    
    if branch:
        branch = branch
    
    msg, employee_response = await employee_service.get_all_employees(
        current_user.tenant_id,
        branch,
        limit, 
        offset, 
        role, 
        status, 
        province, 
        district, 
        gender, 
        start_date, 
        end_date, 
        id, 
        full_name, 
        email,
        phone_number,
        address,
        note,
        query_search
    )
    logger.info("Endpoints: get_all_employees called successfully.")
    return make_response_object(employee_response, msg)

@router.get("/employees/work_on_branch")
async def get_employee_by_branch_name(
    branch: str, 
    user: Employee = Depends(oauth2.get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    
    current_user = await user
    if current_user.role != "Quản lý":
        raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_ACCESS_DENIED)
    
    employee_service = EmployeeService(db=db)
    
    logger.info("Endpoints: get_employee_by_branch_name called.")  
    msg, employee_response = await employee_service.get_employee_by_branch_name(branch)
    logger.info("Endpoints: get_employee_by_branch_name called successfully.")
    return make_response_object(employee_response, msg)
    

@router.get("/employees/{employee_id}")
async def get_employee_by_id(
    employee_id: str, 
    user: Employee = Depends(oauth2.get_current_user),
    branch: str = None,
    db: Session = Depends(get_db)
) -> Any:
    
    current_user = await user
    if current_user.role == "Nhân viên":
        raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_ACCESS_DENIED)
    
    if branch:
        branch = branch
    else:
        branch = current_user.branch
    
    employee_service = EmployeeService(db=db)
    
    logger.info("Endpoints: get_employee_by_id called.")  
    msg, employee_response = await employee_service.get_employee_by_id(employee_id, current_user.branch, branch)
    logger.info("Endpoints: get_all_employees called successfully.")
    return make_response_object(employee_response, msg)
    
@router.put("/employees/{employee_id}")
async def update_employee(
    employee_id: str, 
    employee_update: EmployeeUpdate, 
    user: Employee = Depends(oauth2.get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    
    current_user = await user
    if current_user.role == "Nhân viên":
        raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_ACCESS_DENIED)
    
    employee_service = EmployeeService(db=db)
    
    logger.info("Endpoints: update_employee called.")
    msg, employee_response = await employee_service.update_employee(employee_id, employee_update, branch=current_user.branch)
    logger.info("Endpoints: update_employee called successfully.")
    return make_response_object(employee_response, msg)

@router.delete("/employees/{employee_id}")
async def delete_employee(
    employee_id: str, 
    user: Employee = Depends(oauth2.get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    
    current_user = await user
    if current_user.role == "Nhân viên":
        raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_ACCESS_DENIED)
    
    employee_service = EmployeeService(db=db)
    
    logger.info("Endpoints: delete_employee called.")
    msg, employee_response = await employee_service.delete_employee(employee_id, current_user.branch)
    logger.info("Endpoints: delete_employee called successfully.")
    return make_response_object(employee_response, msg)

# @router.get("/employee/search")
# async def search_employee(
#     user: Employee = Depends(oauth2.get_current_user),
#     db: Session = Depends(get_db), 
#     condition: Optional[str] = Query(None),
#     limit: int = None,
#     offset: int = None
# ) -> Any:
    
#     current_user = await user
#     if current_user.role == "Nhân viên":
#         raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_ACCESS_DENIED)
    
#     employee_service = EmployeeService(db=db)
    
#     logger.info("Endpoints: search_employee called.")
#     msg, employee_response = await employee_service.search_employee(condition, limit, offset)
#     logger.info("Endpoints: search_employee called successfully.")
    
#     return make_response_object(employee_response, msg)

# @router.get("/employees/filter")
# async def filter_employee(
#     user: Employee = Depends(oauth2.get_current_user),
#     db: Session = Depends(get_db),
#     status: str = None,
#     role: str = None,
#     branch_name: str = None,
#     province: str = None,
#     district: str = None
# ) -> Any:
    
#     current_user = await user
#     if current_user.role == "Nhân viên":
#         raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_ACCESS_DENIED)
    
#     employee_service = EmployeeService(db=db)
    
#     logger.info("Endpoints: filter_employee called.")
#     msg, employee_response = await employee_service.filter_employee(status, role, branch_name, province, district)
#     logger.info("Endpoints: filter_employee called successfully.")
    
#     return make_response_object(employee_response, msg)