import logging

from typing import Optional
from pydantic import EmailStr, UUID4

from sqlalchemy.orm import Session
from app.models.order_detail import OrderDetail
from app.schemas.purchase_order import PurchaseOrderCreate, PurchaseOrderUpdate
from app.crud.base import CRUDBase
from ..models import PurchaseOrder

from app.core.exceptions import error_exception_handler
from app.constant.app_status import AppStatus

logger = logging.getLogger(__name__)


class CRUDPurchaseOrder(CRUDBase[PurchaseOrder, PurchaseOrderCreate, PurchaseOrderUpdate]):    
    @staticmethod
    async def get_all_purchase_orders(db: Session) -> Optional[PurchaseOrder]:
        return db.query(PurchaseOrder).all()
    
    @staticmethod
    async def get_purchase_order_by_phone(db: Session, phone_number: str) -> Optional[PurchaseOrder]:
        return db.query(PurchaseOrder).filter(PurchaseOrder.phone_number == phone_number).first()
    
    @staticmethod
    async def get_purchase_order_by_email(db: Session, email: EmailStr) -> Optional[PurchaseOrder]:
        return db.query(PurchaseOrder).filter(PurchaseOrder.email == email).first()
    
    @staticmethod
    async def get_purchase_order_by_id(db: Session, purchase_order_id: str):
        return db.query(PurchaseOrder).filter(PurchaseOrder.id == purchase_order_id).first()
    
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
    def create(db: Session, *, obj_in: PurchaseOrderCreate,obj) -> PurchaseOrder:
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
            purchase_order_id = db_obj.id
            )
               for product in obj]
        
        db.add_all(order_obj)
        db.commit()
        
        logger.info("CRUDPurchaseOrder: create called successfully.")
        return order_obj

purchase_order = CRUDPurchaseOrder(PurchaseOrder)