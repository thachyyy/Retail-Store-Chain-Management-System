import logging

from typing import Optional
from pydantic import EmailStr, UUID4

from sqlalchemy.orm import Session,joinedload

from app.api.endpoints.invoice_for_customer import create_invoice_for_customer
from app.models.order_detail import OrderDetail
from app.schemas.invoice_for_customer import InvoiceForCustomerCreateParams
from app.schemas.purchase_order import PurchaseOrderCreate, PurchaseOrderUpdate
from app.crud.base import CRUDBase
from app.services.invoice_for_customer import InvoiceForCustomerService
from ..models import PurchaseOrder

from app.core.exceptions import error_exception_handler
from app.constant.app_status import AppStatus

logger = logging.getLogger(__name__)


class CRUDPurchaseOrder(CRUDBase[PurchaseOrder, PurchaseOrderCreate, PurchaseOrderUpdate]):    
    @staticmethod
    async def get_all_purchase_orders(db: Session,sql:str,tenant_id:str,branch:str,offset:int= None,limit :int = None) -> Optional[PurchaseOrder]:
        total = db.execute(sql)
        result_as_dict = total.mappings().all()
        
        response = db.query(PurchaseOrder).options(joinedload(PurchaseOrder.customer),joinedload(PurchaseOrder.employee)).filter(PurchaseOrder.tenant_id == tenant_id, PurchaseOrder.branch == branch)
        
        
        if limit is not None and offset is not None:
            response = response.offset(offset).limit(limit)
        return response.all(), result_as_dict
        
    
    @staticmethod
    async def get_purchase_order_by_phone(db: Session, phone_number: str) -> Optional[PurchaseOrder]:
        return db.query(PurchaseOrder).filter(PurchaseOrder.phone_number == phone_number).first()
    
    @staticmethod
    async def get_purchase_order_by_email(db: Session, email: EmailStr) -> Optional[PurchaseOrder]:
        return db.query(PurchaseOrder).filter(PurchaseOrder.email == email).first()
    
    @staticmethod
    async def get_purchase_order_by_id(db: Session, purchase_order_id: str, tenant_id: str):
        return db.query(PurchaseOrder).filter(PurchaseOrder.id == purchase_order_id, PurchaseOrder.tenant_id == tenant_id).first()
    
    @staticmethod
    async def get_last_id(db: Session):
        sql = "SELECT MAX(SUBSTRING(id FROM '[0-9]+')::INT) FROM purchase_order;"
        last_id = db.execute(sql).scalar_one_or_none()
        if last_id is None:
            return 0
        return last_id
    
    @staticmethod
    async def update_purchase_order(db: Session, purchase_order_id: str, purchase_order_update: PurchaseOrderUpdate):
        update_data = purchase_order_update.dict(exclude_unset=True)
        return db.query(PurchaseOrder).filter(PurchaseOrder.id == purchase_order_id).update(update_data)
    
    @staticmethod
    async def delete_purchase_order(db: Session, purchase_order_id: str):
        try:
            return db.query(PurchaseOrder).filter(PurchaseOrder.id == purchase_order_id).delete()
        except:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_DATA_USED_ERROR)
    
    @staticmethod
    async def get_purchase_order_by_conditions(db: Session, sql: str, total: str):        
        result = db.execute(sql)
        sum = db.execute(total)
        sum = sum.mappings().all()
        result_as_dict = result.mappings().all()
        return result_as_dict, sum
    
    @staticmethod
    async def create(db: Session, *,
                     paid, 
                     obj_in: PurchaseOrderCreate,
                     obj,
                     tenant_id:str
                     ) -> PurchaseOrder:
        logger.info("CRUDPurchaseOrder: create called.")
        logger.debug("With: PurchaseOrderCreate - %s", obj_in.dict())

        db_obj = PurchaseOrder(**obj_in.dict())
        db.add(db_obj)
        db.flush()
        db.refresh(db_obj)
        order_obj = [ OrderDetail(
            quantity = product.quantity,
            sub_total = product.sub_total,
            price = product.price,
            batch_id = product.batch,
            product_id = product.product_id,
            product_name = product.product_name,
            purchase_order_id = db_obj.id,
            tenant_id = tenant_id,
            branch = obj_in.branch
            )
               for product in obj]
        
        db.add_all(order_obj)
        db.commit()
        
        list_order = []
        for item in order_obj:
            list_order += [item.id]
        
        invoice_for_customer_obj = InvoiceForCustomerCreateParams(
            total=obj_in.total,
            status = obj_in.status,
            payment_method = "Tiền mặt",
            belong_to_order = obj_in.id,
            order_detail = list_order,
            tenant_id = tenant_id,
        )
        

        invoice_for_customer_service = InvoiceForCustomerService(db=db)
        await invoice_for_customer_service.create_invoice_for_customer(paid,invoice_for_customer_obj,tenant_id,obj_in.branch)
        logger.info("CRUDPurchaseOrder: create called successfully.")
        return order_obj

purchase_order = CRUDPurchaseOrder(PurchaseOrder)