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
    async def get_all_employees(
        db: Session,
        offset: int = None,
        limit: int = None
    ) -> Optional[Employee]:
        result = db.query(Employee)
        
        if offset is not None and limit is not None:
            result = result.offset(offset).limit(limit)
            
        return result.all()
    
    @staticmethod
    async def get_employee_by_id(db: Session, id: str, branch: str = None):   
        if branch:
            return db.query(Employee).filter(Employee.id == id, Employee.branch == branch).first()
        else:
            return db.query(Employee).filter(Employee.id == id).first()
    
    @staticmethod
    async def get_employee_by_branch_name(db: Session, branch_name: str):
        logger.info("CRUDEmployee: get_employee_by_branch_name called.")
        current_employee_by_branch_name =  db.query(Employee).filter(Employee.branch == branch_name).all()
        logger.info("CRUDEmployee: get_employee_by_branch_name called successfully.")
        return current_employee_by_branch_name
    
    @staticmethod
    async def get_employee_by_email(db: Session, email: str, id: str = None):
        if id is not None:
            return db.query(Employee).filter(Employee.email == email, Employee.id != id).first()
        else:
            return db.query(Employee).filter(Employee.email == email).first()
    
    @staticmethod
    async def get_employee_by_phone(db: Session, phone_number: str, id: str = None):
        if id is not None:
            return db.query(Employee).filter(Employee.phone_number == phone_number, Employee.id != id).first()
        else:
            return db.query(Employee).filter(Employee.phone_number == phone_number).first()
    
    @staticmethod
    async def get_last_id(db: Session):
        sql = "SELECT MAX(SUBSTRING(id FROM '[0-9]+')::INT) FROM employee;"
        last_id = db.execute(sql).scalar_one_or_none()
        if last_id is None:
            return 0
        return last_id
    
    @staticmethod
    async def create(db: Session, *, obj_in: EmployeeCreate) -> Employee:
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
        update_data = employee_update.dict(exclude_unset=True)
        return db.query(Employee).filter(Employee.id == employee_id).update(update_data)
    
    @staticmethod
    async def delete_employee(db: Session, employee_id: str):
        return db.query(Employee).filter(Employee.id == employee_id).delete()
    
    @staticmethod
    async def get_employee_by_conditions(db: Session, sql: str, total: str):        
        result = db.execute(sql)
        sum = db.execute(total)
        sum = sum.mappings().all()
        result_as_dict = result.mappings().all()
        return result_as_dict, sum
    
employee = CRUDEmployee(Employee)