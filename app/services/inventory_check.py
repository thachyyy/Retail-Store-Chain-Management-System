import logging
from typing import List
import uuid
from fastapi import HTTPException
from sqlalchemy.orm import Session
from pydantic import UUID4

from app import crud
from app.constant.app_status import AppStatus
from app.schemas.inventory_check import InventoryCheck, InventoryCheckResponse
from app.core.exceptions import error_exception_handler

logger = logging.getLogger(__name__)

class InventoryCheckService:
    def __init__(self, db: Session):
        self.db = db
        
    async def inventory_check(self, obj_in: list[InventoryCheck], tenant_id: str, branch: str):
        logger.info("InventoryCheckService: inventory_check is called.")
        
        response: List[InventoryCheckResponse] = []
        
        for item in obj_in:
            quantity_in_db = await crud.inventory_check.get_quantity_in_db(self.db, tenant_id, branch, item.batch_id, item.product_id)
            real_quantity = int(item.quantity)
            res = InventoryCheckResponse(
                branch_id=item.branch_id,
                product_id=item.product_id,
                batch_id=item.batch_id,
                real_quantity=real_quantity,
                quantiry_in_db=quantity_in_db,
                difference= abs(quantity_in_db - real_quantity)
            )
            response.append(res)
        
        logger.info("InventoryCheckService: inventory_check is called successfully.")
        
        return response