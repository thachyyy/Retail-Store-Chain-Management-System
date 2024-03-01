import logging

from typing import Optional
from pydantic import EmailStr, UUID4

from sqlalchemy.orm import Session
from app.schemas.customer import CustomerCreate, CustomerUpdate
from app.crud.base import CRUDBase
from ..models import Customer

logger = logging.getLogger(__name__)


class CRUDCustomer(CRUDBase[Customer, CustomerCreate, CustomerUpdate]):    
    @staticmethod
    async def get_all_customers(db: Session) -> Optional[Customer]:
        return db.query(Customer).all()
    
    @staticmethod
    async def get_customer_by_phone(db: Session, phone_number: str) -> Optional[Customer]:
        return db.query(Customer).filter(Customer.phone_number == phone_number).first()
    
    @staticmethod
    async def get_customer_by_email(db: Session, email: EmailStr) -> Optional[Customer]:
        return db.query(Customer).filter(Customer.email == email).first()
    
    @staticmethod
    async def get_customer_by_id(db: Session, customer_id: str):
        return db.query(Customer).filter(Customer.id == customer_id).first()
    
    @staticmethod
    async def update_customer(db: Session, customer_id: str, customer_update: CustomerUpdate):
        update_data = customer_update.dict(exclude_none=True)
        return db.query(Customer).filter(Customer.id == customer_id).update(update_data)
    
    @staticmethod
    async def delete_customer(db: Session, customer_id: str):
        return db.query(Customer).filter(Customer.id == customer_id).delete()
    
    @staticmethod
    async def search_customer(db: Session, sql: str):        
        result = db.execute(sql)
        result_as_dict = result.mappings().all()
        return result_as_dict
    
    @staticmethod
    async def filter_customer(db: Session, sql: str):
        result = db.execute(sql)
        result_as_dict = result.mappings().all()
        return result_as_dict
    
    @staticmethod
    def create(db: Session, *, obj_in: CustomerCreate) -> Customer:
        logger.info("CRUDCustomer: create called.")
        logger.debug("With: CustomerCreate - %s", obj_in.dict())

        db_obj = Customer(**obj_in.dict())
        db.add(db_obj)
        db.flush()
        db.refresh(db_obj)
        logger.info("CRUDCustomer: create called successfully.")
        return db_obj

customer = CRUDCustomer(Customer)
