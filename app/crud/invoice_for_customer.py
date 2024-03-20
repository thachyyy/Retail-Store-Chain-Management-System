import logging

from typing import Optional
from pydantic import EmailStr, UUID4

from sqlalchemy.orm import Session
from app.schemas.invoice_for_customer import InvoiceForCustomerCreate, InvoiceForCustomerUpdate
from app.crud.base import CRUDBase
from ..models import InvoiceForCustomer

logger = logging.getLogger(__name__)


class CRUDInvoiceForCustomer(CRUDBase[InvoiceForCustomer, InvoiceForCustomerCreate, InvoiceForCustomerUpdate]):    
    @staticmethod
    async def get_all_invoice_for_customers(db: Session) -> Optional[InvoiceForCustomer]:
        return db.query(InvoiceForCustomer).all()
    
    @staticmethod
    async def get_invoice_for_customer_by_phone(db: Session, phone_number: str) -> Optional[InvoiceForCustomer]:
        return db.query(InvoiceForCustomer).filter(InvoiceForCustomer.phone_number == phone_number).first()
    
    @staticmethod
    async def get_invoice_for_customer_by_email(db: Session, email: EmailStr) -> Optional[InvoiceForCustomer]:
        return db.query(InvoiceForCustomer).filter(InvoiceForCustomer.email == email).first()
    
    @staticmethod
    async def get_invoice_for_customer_by_id(db: Session, invoice_for_customer_id: str):
        return db.query(InvoiceForCustomer).filter(InvoiceForCustomer.id == invoice_for_customer_id).first()
    
    @staticmethod
    async def get_last_id(db: Session):
        sql = "SELECT MAX(SUBSTRING(id FROM '[0-9]+')::INT) FROM invoice_for_customer;"
        last_id = db.execute(sql).scalar_one_or_none()
        if last_id is None:
            return 0
        return last_id
    
    @staticmethod
    async def update_invoice_for_customer(db: Session, invoice_for_customer_id: str, invoice_for_customer_update: InvoiceForCustomerUpdate):
        update_data = invoice_for_customer_update.dict(exclude_none=True)
        return db.query(InvoiceForCustomer).filter(InvoiceForCustomer.id == invoice_for_customer_id).update(update_data)
    
    @staticmethod
    async def delete_invoice_for_customer(db: Session, invoice_for_customer_id: str):
        return db.query(InvoiceForCustomer).filter(InvoiceForCustomer.id == invoice_for_customer_id).delete()
    
    @staticmethod
    async def search_invoice_for_customer(db: Session, sql: str):        
        result = db.execute(sql)
        result_as_dict = result.mappings().all()
        return result_as_dict
    
    @staticmethod
    async def filter_invoice_for_customer(db: Session, sql: str):
        result = db.execute(sql)
        result_as_dict = result.mappings().all()
        return result_as_dict
    
    @staticmethod
    def create(db: Session, *, obj_in: InvoiceForCustomerCreate) -> InvoiceForCustomer:
        logger.info("CRUDInvoiceForCustomer: create called.")
        logger.debug("With: InvoiceForCustomerCreate - %s", obj_in.dict())

        db_obj = InvoiceForCustomer(**obj_in.dict())
        db.add(db_obj)
        db.flush()
        db.refresh(db_obj)
        logger.info("CRUDInvoiceForCustomer: create called successfully.")
        return db_obj

invoice_for_customer = CRUDInvoiceForCustomer(InvoiceForCustomer)
