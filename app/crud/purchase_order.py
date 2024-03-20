import logging

from typing import Optional
from pydantic import EmailStr, UUID4

from sqlalchemy.orm import Session
from app.schemas.purchase_order import PurchaseOrderCreate, PurchaseOrderUpdate
from app.crud.base import CRUDBase
from ..models import PurchaseOrder

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
        update_data = purchase_order_update.dict(exclude_none=True)
        return db.query(PurchaseOrder).filter(PurchaseOrder.id == purchase_order_id).update(update_data)
    
    @staticmethod
    async def delete_purchase_order(db: Session, purchase_order_id: str):
        return db.query(PurchaseOrder).filter(PurchaseOrder.id == purchase_order_id).delete()
    
    @staticmethod
    async def search_purchase_order(db: Session, sql: str):        
        result = db.execute(sql)
        result_as_dict = result.mappings().all()
        return result_as_dict
    
    @staticmethod
    async def filter_purchase_order(db: Session, sql: str):
        result = db.execute(sql)
        result_as_dict = result.mappings().all()
        return result_as_dict
    
    @staticmethod
    def create(db: Session, *, obj_in: PurchaseOrderCreate) -> PurchaseOrder:
        logger.info("CRUDPurchaseOrder: create called.")
        logger.debug("With: PurchaseOrderCreate - %s", obj_in.dict())

        db_obj = PurchaseOrder(**obj_in.dict())
        db.add(db_obj)
        db.flush()
        db.refresh(db_obj)
        logger.info("CRUDPurchaseOrder: create called successfully.")
        return db_obj

purchase_order = CRUDPurchaseOrder(PurchaseOrder)