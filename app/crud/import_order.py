import logging

from typing import Optional
from sqlalchemy.orm import Session
from pydantic import UUID4

from app.schemas.import_order import ImportOrderCreate, ImportOrderUpdate
from app.crud.base import CRUDBase
from ..models import ImportOrder

logger = logging.getLogger(__name__)

class CRUDImportOrder(CRUDBase[ImportOrder, ImportOrderCreate, ImportOrderUpdate]):
    @staticmethod
    async def get_all_import_orders(db: Session) -> Optional[ImportOrder]:
        return db.query(ImportOrder).all()
    
    @staticmethod
    async def get_import_order_by_id(db: Session, import_order_id: str):
        return db.query(ImportOrder).filter(ImportOrder.id == import_order_id).first()
    
    @staticmethod
    async def get_last_id(db: Session):
        sql = "SELECT MAX(SUBSTRING(id FROM '[0-9]+')::INT) FROM import_order;"
        last_id = db.execute(sql).scalar_one_or_none()
        if last_id is None:
            return 0
        return last_id
    
    @staticmethod
    def create(db: Session, *, obj_in: ImportOrderCreate) -> ImportOrder:
        logger.info("CRUDImportOrder: create called.")
        logger.debug("With: ImportOrderCreate - %s", obj_in.dict())

        db_obj = ImportOrder(**obj_in.dict())
        db.add(db_obj)
        db.flush()
        db.refresh(db_obj)
        logger.info("CRUDImportOrder: create called successfully.")
        return db_obj
 
    @staticmethod
    async def update_import_order(db: Session, import_order_id: str, import_order_update: ImportOrderUpdate):
        update_data = import_order_update.dict(exclude_unset=True)
        return db.query(ImportOrder).filter(ImportOrder.id == import_order_id).update(update_data)
    
    @staticmethod
    async def delete_import_order(db: Session, import_order_id: str):
        return db.query(ImportOrder).filter(ImportOrder.id == import_order_id).delete()
    
import_order = CRUDImportOrder(ImportOrder)