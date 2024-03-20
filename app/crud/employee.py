import logging
from fastapi import HTTPException
from typing import Optional
from sqlalchemy.orm import Session
from app.constant.app_status import AppStatus
from app.core.exceptions import error_exception_handler

from app.schemas.employee import EmployeeCreate, EmployeeUpdate
from app.crud.base import CRUDBase
from ..models import Employee

logger = logging.getLogger(__name__)

class CRUDEmployee(CRUDBase[Employee, EmployeeCreate, EmployeeUpdate]):
    @staticmethod
    async def get_all_employees(db: Session) -> Optional[Employee]:
        return db.query(Employee).all()
    
    @staticmethod
    async def get_employee_by_id(db: Session, employee_id: str):
        logger.info("CRUDEmployee: get_employee_by_id called.")
        current_employee_by_id =  db.query(Employee).filter(Employee.id == employee_id).first()
        if not current_employee_by_id:
                raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_EMPLOYEE_NOT_FOUND)
        logger.info("CRUDEmployee: get_employee_by_id called successfully.")
        return current_employee_by_id
    
    @staticmethod
    async def get_employee_by_branch_name(db: Session, branch_name: str):
        logger.info("CRUDEmployee: get_employee_by_branch_name called.")
        current_employee_by_branch_name =  db.query(Employee).filter(Employee.branch_name == branch_name).all()
        if not current_employee_by_branch_name:
                raise HTTPException(status_code =404, detail="Chi nhánh chưa có nhân viên")
        logger.info("CRUDEmployee: get_employee_by_branch_name called successfully.")
        return current_employee_by_branch_name
    
    @staticmethod
    async def get_employee_by_email(db: Session, email: str):
        return db.query(Employee).filter(Employee.email == email).first()
    
    @staticmethod
    async def get_employee_by_phone(db: Session, phone_number: str):
        return db.query(Employee).filter(Employee.phone_number == phone_number).first()
    
    @staticmethod
    async def get_last_id(db: Session):
        sql = "SELECT MAX(SUBSTRING(id FROM '[0-9]+')::INT) FROM employee;"
        last_id = db.execute(sql).scalar_one_or_none()
        if last_id is None:
            return 0
        return last_id
    
    @staticmethod
    def create(db: Session, *, obj_in: EmployeeCreate) -> Employee:
        logger.info("CRUDEmployee: create called.")
        logger.debug("With: EmployeeCreate - %s", obj_in.dict())

        db_obj = Employee(**obj_in.dict())
        db.add(db_obj)
        db.flush()
        db.refresh(db_obj)
        logger.info("CRUDEmployee: create called successfully.")
        return db_obj
    
    @staticmethod
    async def update_employee(db: Session, employee_id: str, employee_update: EmployeeUpdate):
        update_data = employee_update.dict(exclude_none=True)
        return db.query(Employee).filter(Employee.id == employee_id).update(update_data)
    
    @staticmethod
    async def delete_employee(db: Session, employee_id: str):
        return db.query(Employee).filter(Employee.id == employee_id).delete()
    
    @staticmethod
    async def search_employee(db: Session, sql: str):        
        result = db.execute(sql)
        result_as_dict = result.mappings().all()
        return result_as_dict
    
    @staticmethod
    async def filter_employee(db: Session, sql: str):
        result = db.execute(sql)
        result_as_dict = result.mappings().all()
        return result_as_dict
    
employee = CRUDEmployee(Employee)