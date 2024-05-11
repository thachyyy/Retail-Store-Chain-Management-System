import logging
from fastapi import HTTPException
from typing import Optional
from sqlalchemy.orm import Session
from app.constant.app_status import AppStatus
from app.core.exceptions import error_exception_handler

from app.schemas.inventory_check import InventoryCheck, InventoryCheckResponse
from app.crud.base import CRUDBase
from datetime import date
from app.core.exceptions import error_exception_handler
from ..models import InventoryCheck

logger = logging.getLogger(__name__)

class CRUDInventoryCheck():
    @staticmethod
    def get_multi(
        db: Session, *, skip: int = None, limit: int = None, tenant_id: str, branch: str = None
    ):
        if branch:
            query_set = db.query(InventoryCheck).filter(InventoryCheck.tenant_id == tenant_id, InventoryCheck.branch == branch)
        else:  
            query_set = db.query(InventoryCheck).filter(InventoryCheck.tenant_id == tenant_id)
        count = query_set.count()

        if skip is not None and limit is not None:
            query_set = query_set.offset(skip).limit(limit)

        return query_set.all(), count
    
    @staticmethod
    async def get_quantity_in_db(db: Session, tenant_id: str, branch: str, batch_id: str, product_id: str):
        sql = f"""SELECT quantity 
                  FROM public.batch
                  WHERE tenant_id = '{tenant_id}'
                    AND branch = '{branch}'
                    AND id = '{batch_id}'
                    AND product_id = '{product_id}';
        """
        
        result = db.execute(sql).fetchone()
        if result:
            quantity = int(result[0])
        else:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_BATCH_NOT_FOUND)
        return quantity
    
    @staticmethod
    def create(db: Session, *, obj_in: InventoryCheckResponse):
        logger.info("CRUDInventoryCheck: create called.")
        logger.debug("With: InventoryCheckCreate - %s", obj_in.dict())

        db_obj = InventoryCheck(**obj_in.dict())
        db.add(db_obj)
        db.flush()
        db.refresh(db_obj)
        logger.info("CRUDInventoryCheck: create called successfully.")
        return db_obj
    
    @staticmethod
    async def get_inventory_check_by_id(db: Session, id: str, tenant_id: str):
        return db.query(InventoryCheck).filter(InventoryCheck.id == id, InventoryCheck.tenant_id == tenant_id).first()
    
    @staticmethod
    async def delete_inventory_check(db: Session, id: str):
        return db.query(InventoryCheck).filter(InventoryCheck.id == id).delete()

inventory_check = CRUDInventoryCheck()