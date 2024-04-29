import logging
from fastapi import HTTPException
from typing import Optional
from sqlalchemy.orm import Session
from app.constant.app_status import AppStatus
from app.core.exceptions import error_exception_handler

from app.schemas.inventory_check import InventoryCheck
from app.crud.base import CRUDBase
from datetime import date
from app.core.exceptions import error_exception_handler

logger = logging.getLogger(__name__)

class CRUDInventoryCheck():
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

inventory_check = CRUDInventoryCheck()