from datetime import date, datetime
import logging

from typing import Optional
from pydantic import EmailStr, UUID4

from sqlalchemy import func
from sqlalchemy.orm import Session,joinedload
from app.models.order_detail import OrderDetail
from app.schemas.invoice_for_customer import InvoiceForCustomerCreate, InvoiceForCustomerUpdate
from app.crud.base import CRUDBase
from ..models import InvoiceForCustomer
from ..models import OrderDetail

logger = logging.getLogger(__name__)


class CRUDInvoiceForCustomer(CRUDBase[InvoiceForCustomer, InvoiceForCustomerCreate, InvoiceForCustomerUpdate]):    
    
    @staticmethod
    async def get_total_sale_by_all_branch(db:Session, tenant_id: str ,start_date:date ,end_date:date):
        start_datetime = datetime.combine(start_date, datetime.min.time())  # Sets time to 00:00:00
        end_datetime = datetime.combine(end_date, datetime.max.time())
        
        query = db.query(InvoiceForCustomer).filter( \
        InvoiceForCustomer.created_at.between(start_datetime, end_datetime),
        InvoiceForCustomer.tenant_id == tenant_id,
        InvoiceForCustomer.status == 'Đã thanh toán')

        total_sale = db.query(func.sum(InvoiceForCustomer.total)).filter( \
        InvoiceForCustomer.created_at.between(start_datetime, end_datetime),
        InvoiceForCustomer.tenant_id == tenant_id,
        InvoiceForCustomer.status == 'Đã thanh toán').scalar()
        
        
        
        if total_sale is None:
            total_sale = 0 
        return query.all(),total_sale        
                           
    @staticmethod
    async def get_total_sale_by_branch(db:Session, tenant_id: str , branch:str,start_date:date ,end_date:date):
        start_datetime = datetime.combine(start_date, datetime.min.time())  # Sets time to 00:00:00
        end_datetime = datetime.combine(end_date, datetime.max.time())
        
        query = db.query(InvoiceForCustomer).filter( \
        InvoiceForCustomer.created_at.between(start_datetime, end_datetime),
        InvoiceForCustomer.tenant_id == tenant_id,
        InvoiceForCustomer.branch == branch)
        
        total_sale = db.query(func.sum(InvoiceForCustomer.total)).filter( \
        InvoiceForCustomer.created_at.between(start_datetime, end_datetime),
        InvoiceForCustomer.tenant_id == tenant_id,
        InvoiceForCustomer.branch == branch).scalar()
        if total_sale is None:
            total_sale = 0 
        return query.all(),total_sale        
                           
    @staticmethod
    async def get_all_invoice_for_customers(db: Session, tenant_id: str, branch: str, sql:str, offset: int = None, limit: int = None) -> Optional[InvoiceForCustomer]:
        
        total = db.execute(sql)
        result_as_dict = total.mappings().all()
        
        response = db.query(InvoiceForCustomer).filter(InvoiceForCustomer.tenant_id == tenant_id, InvoiceForCustomer.branch == branch)
        
        if limit is not None and offset is not None:
               response = response.offset(offset).limit(limit)
        return response.all(), result_as_dict
    
    @staticmethod
    async def get_order_detail_by_id(db: Session, id: int):
        return db.query(OrderDetail).filter(OrderDetail.id == id).first()
    
    @staticmethod
    async def get_invoice_for_customer_by_phone(db: Session, phone_number: str, tenant_id: str) -> Optional[InvoiceForCustomer]:
        return db.query(InvoiceForCustomer).filter(InvoiceForCustomer.phone_number == phone_number, InvoiceForCustomer.tenant_id == tenant_id).first()
    
    @staticmethod
    async def get_invoice_for_customer_by_email(db: Session, email: EmailStr, tenant_id: str) -> Optional[InvoiceForCustomer]:
        return db.query(InvoiceForCustomer).filter(InvoiceForCustomer.email == email, InvoiceForCustomer.tenant_id == tenant_id).first()
    
    @staticmethod
    async def get_invoice_for_customer_by_id(db: Session, invoice_for_customer_id: str, tenant_id: str):
        return db.query(InvoiceForCustomer).options(joinedload(InvoiceForCustomer.purchase_order)).where(InvoiceForCustomer.id == invoice_for_customer_id, InvoiceForCustomer.tenant_id == tenant_id).one()
    
    @staticmethod
    async def get_last_id(db: Session):
        sql = "SELECT MAX(SUBSTRING(id FROM '[0-9]+')::INT) FROM invoice_for_customer;"
        last_id = db.execute(sql).scalar_one_or_none()
        if last_id is None:
            return 0
        return last_id
    
    @staticmethod
    async def update_invoice_for_customer(db: Session, invoice_for_customer_id: str, invoice_for_customer_update: InvoiceForCustomerUpdate):
        update_data = invoice_for_customer_update.dict(exclude_unset=True)
        return db.query(InvoiceForCustomer).filter(InvoiceForCustomer.id == invoice_for_customer_id).update(update_data)
    
    @staticmethod
    async def delete_invoice_for_customer(db: Session, invoice_for_customer_id: str):
        return db.query(InvoiceForCustomer).filter(InvoiceForCustomer.id == invoice_for_customer_id).delete()
    
    # @staticmethod
    # async def search_invoice_for_customer(db: Session, sql: str):        
    #     result = db.execute(sql)
    #     result_as_dict = result.mappings().all()
    #     return result_as_dict
    
    # @staticmethod
    # async def filter_invoice_for_customer(db: Session, sql: str):
    #     result = db.execute(sql)
    #     result_as_dict = result.mappings().all()
    #     return result_as_dict
    
    @staticmethod
    async def get_invoice_for_customer_by_conditions(db: Session, sql: str, total: str):        
        result = db.execute(sql)
        sum = db.execute(total)
        sum = sum.mappings().all()
        result_as_dict = result.mappings().all()
        return result_as_dict, sum
    
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
    
    @staticmethod
    async def get_customer_name(db: Session, purchase_order_id: str):
        sql = f"""select c.full_name
                  from purchase_order po 
                  join customer c on po.belong_to_customer = c.id
                  where po.id = '{purchase_order_id}';
        """
        
        result = db.execute(sql).fetchone()
        
        if result:
            return result[0]
        else: return None

invoice_for_customer = CRUDInvoiceForCustomer(InvoiceForCustomer)
