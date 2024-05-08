import logging

from typing import Optional
from sqlalchemy.orm import Session
from pydantic import UUID4
from datetime import date

from app.schemas.import_order import ImportOrderCreate, ImportOrderUpdate
from app.crud.base import CRUDBase
from ..models import ImportOrder

logger = logging.getLogger(__name__)

class CRUDImportOrder(CRUDBase[ImportOrder, ImportOrderCreate, ImportOrderUpdate]):
    @staticmethod
    async def get_all_import_orders(db: Session) -> Optional[ImportOrder]:
        return db.query(ImportOrder).all()
    
    @staticmethod
    async def get_import_order_by_id(db: Session, id: str,branch: str, tenant_id: str):
        return db.query(ImportOrder).filter(ImportOrder.id == id,ImportOrder.branch == branch,ImportOrder.tenant_id == tenant_id,).first()
    
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
    async def update_import_order(db: Session, id: str, import_order_update: ImportOrderUpdate):
        update_data = import_order_update.dict(exclude_unset=True)
        return db.query(ImportOrder).filter(ImportOrder.id == id).update(update_data)
    
    @staticmethod
    async def delete_import_order(db: Session, id: str):
        return db.query(ImportOrder).filter(ImportOrder.id == id).delete()
    
    @staticmethod
    async def get_period_contract(db: Session, id: str):
        sql = f"SELECT period FROM public.contract_for_vendor WHERE id = '{id}';"
        result = db.execute(sql).fetchone()
        if result:
            return result[0]  # Chuyển kết quả thành chuỗi
        return None
    
    @staticmethod
    async def update_date_import(db: Session, id: str, latest_import: date, next_import: date):
        try:
            sql = f"UPDATE public.contract_for_vendor SET latest_import = '{latest_import}' AND next_import = '{next_import}' WHERE id = '{id}';"
            db.execute(sql)
            db.commit()
            return "Success"
        except Exception as e:
            db.rollback()
            print("Exception when update date import", e)
        
    
import_order = CRUDImportOrder(ImportOrder)