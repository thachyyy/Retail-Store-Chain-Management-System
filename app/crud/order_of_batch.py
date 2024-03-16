import logging

from pydantic import EmailStr
from typing import Optional
from sqlalchemy.orm import Session

from app.schemas.order_of_batch import OrderOfBatchCreate, OrderOfBatchUpdate
from app.crud.base import CRUDBase
from ..models import OrderOfBatch

logger = logging.getLogger(__name__)

class CRUDOrderOfBatch(CRUDBase[OrderOfBatch, OrderOfBatchCreate, OrderOfBatchUpdate]):
    @staticmethod
    async def get_all_order_of_batches(db: Session) -> Optional[OrderOfBatch]:
        return db.query(OrderOfBatch).all()
    
    @staticmethod
    async def get_order_of_batch_by_id(db: Session, order_of_batch_id: str):
        return db.query(OrderOfBatch).filter(OrderOfBatch.id == order_of_batch_id).first()
    
    
    @staticmethod
    def create(db: Session, *, obj_in: OrderOfBatchCreate) -> OrderOfBatch:
        logger.info("CRUDOrderOfBatch: create called.")
        logger.debug("With: OrderOfBatchCreate - %s", obj_in.dict())

        db_obj = OrderOfBatch(**obj_in.dict())
        db.add(db_obj)
        db.flush()
        db.refresh(db_obj)
        logger.info("CRUDOrderOfBatch: create called successfully.")
        return db_obj
    
    @staticmethod
    async def update_order_of_batch(db: Session, order_of_batch_id: str, order_of_batch_update: OrderOfBatchUpdate):
        update_data = order_of_batch_update.dict(exclude_none=True)
        return db.query(OrderOfBatch).filter(OrderOfBatch.id == order_of_batch_id).update(update_data)
    
    @staticmethod
    async def delete_order_of_batch(db: Session, order_of_batch_id: str):
        return db.query(OrderOfBatch).filter(OrderOfBatch.id == order_of_batch_id).delete()
    
    
    
order_of_batch = CRUDOrderOfBatch(OrderOfBatch)