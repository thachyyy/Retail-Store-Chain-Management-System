import logging

from typing import Any, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from pydantic import UUID4
from datetime import date

from app.api.depends import oauth2
# from app.api.depends.oauth2 import create_access_token, create_refresh_token, verify_refresh_token
from app.constant.app_status import AppStatus
from app.core.exceptions import error_exception_handler
from app.db.database import get_db
from app.schemas.employee import EmployeeCreateParams, EmployeeUpdate
from app.services.employee import EmployeeService
from app.utils.response import make_response_object

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/employees")
async def create_employee(
    employee_create: EmployeeCreateParams,
    db: Session = Depends(get_db)
) -> Any:
    employee_service = EmployeeService(db=db)
    logger.info("Endpoints: create_employee called.")
    
    msg,employee_response = await employee_service.create_employee(employee_create)
    logger.info("Endpoints: create_employee called successfully.")
    return make_response_object(employee_response,msg)

@router.get("/employees")
async def get_all_employees(
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
    branch_name: str = None,
    
) -> Any:
    employee_service = EmployeeService(db=db)
    logger.info("Endpoints: get_all_employees called.")
    
    msg, employee_response = await employee_service.get_all_employees(
        limit, 
        offset, 
        status, 
        role, 
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
        branch_name
    )
    logger.info("Endpoints: get_all_employees called successfully.")
    return make_response_object(employee_response, msg)

@router.get("/employees/work_on_branch")
async def get_employee_by_branch_name(branch_name: str, db: Session = Depends(get_db)) -> Any:
    employee_service = EmployeeService(db=db)
    
    logger.info("Endpoints: get_employee_by_branch_name called.")  
    msg, employee_response = await employee_service.get_employee_by_branch_name(branch_name)
    logger.info("Endpoints: get_employee_by_branch_name called successfully.")
    return make_response_object(employee_response, msg)
    

@router.get("/employees/{employee_id}")
async def get_employee_by_id(employee_id: str, db: Session = Depends(get_db)) -> Any:
    employee_service = EmployeeService(db=db)
    
    logger.info("Endpoints: get_employee_by_id called.")  
    msg, employee_response = await employee_service.get_employee_by_id(employee_id)
    logger.info("Endpoints: get_all_employees called successfully.")
    return make_response_object(employee_response, msg)
    
@router.put("/employees/{employee_id}")
async def update_employee(employee_id: str, employee_update: EmployeeUpdate, db: Session = Depends(get_db)) -> Any:
    employee_service = EmployeeService(db=db)
    
    logger.info("Endpoints: update_employee called.")
    msg, employee_response = await employee_service.update_employee(employee_id, employee_update)
    logger.info("Endpoints: update_employee called successfully.")
    return make_response_object(employee_response, msg)

@router.delete("/employees/{employee_id}")
async def delete_employee(employee_id: str, db: Session = Depends(get_db)) -> Any:
    employee_service = EmployeeService(db=db)
    
    logger.info("Endpoints: delete_employee called.")
    msg, employee_response = await employee_service.delete_employee(employee_id)
    logger.info("Endpoints: delete_employee called successfully.")
    return make_response_object(employee_response, msg)

@router.get("/employees/search")
async def search_employee(
    db: Session = Depends(get_db), 
    condition: Optional[str] = Query(None),
    limit: int = None,
    offset: int = None
) -> Any:
    employee_service = EmployeeService(db=db)
    
    logger.info("Endpoints: search_employee called.")
    msg, employee_response = await employee_service.search_employee(condition, limit, offset)
    logger.info("Endpoints: search_employee called successfully.")
    
    return make_response_object(employee_response, msg)

@router.get("/employees/filter")
async def filter_employee(
    db: Session = Depends(get_db),
    status: str = None,
    role: str = None,
    branch_name: str = None,
    province: str = None,
    district: str = None
) -> Any:
    employee_service = EmployeeService(db=db)
    
    logger.info("Endpoints: filter_employee called.")
    msg, employee_response = await employee_service.filter_employee(status, role, branch_name, province, district)
    logger.info("Endpoints: filter_employee called successfully.")
    
    return make_response_object(employee_response, msg)