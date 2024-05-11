import logging
from typing import List
import uuid
from fastapi import HTTPException
from sqlalchemy.orm import Session
from pydantic import UUID4

from app import crud
from app.constant.app_status import AppStatus
from app.schemas.inventory_check import InventoryCheck, InventoryCheckResponse, InventoryCheckCreate
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
            
            obj_create = InventoryCheckCreate(
                branch_id=item.branch_id,
                product_id=item.product_id,
                batch_id=item.batch_id,
                real_quantity=real_quantity,
                quantiry_in_db=quantity_in_db,
                difference= abs(quantity_in_db - real_quantity),
                tenant_id= tenant_id,
                branch=branch
            )
            
            crud.inventory_check.create(db=self.db, obj_in=obj_create)
            self.db.commit()
        
        logger.info("InventoryCheckService: inventory_check is called successfully.")
        
        return response
    
    async def get_all_inventory_check(
        self, 
        tenant_id: str, 
        branch: str = None,
        limit: int = None,
        offset: int = None
    ):
        logger.info("Services: get all inventory check is called.")
        if limit is not None and offset is not None:
            result, total = crud.inventory_check.get_multi(db=self.db, skip=offset*limit,limit=limit, tenant_id=tenant_id, branch=branch)
            
        else:
            result, total = crud.inventory_check.get_multi(db=self.db, tenant_id=tenant_id, branch=branch)
            
        
        logger.info("Services: get all inventory check is called successfully.")
        return dict(message_code=AppStatus.SUCCESS.message,total=total), result
    
    async def get_inventory_check_by_id(
        self, 
        tenant_id: str, 
        id: str
    ):
        logger.info("Services: get_inventory_check_by_id called.")
        result = await crud.inventory_check.get_inventory_check_by_id(db=self.db, id=id, tenant_id=tenant_id)
        logger.info("Services: get_inventory_check_by_id called successfully.")
        if not result:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_INVENTORY_CHECK_NOT_FOUND)
        
        return dict(message_code=AppStatus.SUCCESS.message), result
        
    async def delete_inventory_check(self, tenant_id: str, inventory_check_id: str):
        logger.info("InventoryCheckService: get_inventory_check_by_id called.")
        isValidInventoryCheck = await crud.inventory_check.get_inventory_check_by_id(db=self.db, tenant_id=tenant_id, id=inventory_check_id)
        logger.info("InventoryCheckService: get_inventory_check_by_id called successfully.")
        
        if not isValidInventoryCheck:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_INVENTORY_CHECK_NOT_FOUND)
        
        obj_del = await crud.inventory_check.get_inventory_check_by_id(self.db, inventory_check_id, tenant_id)
        
        logger.info("InventoryCheckService: delete_inventory_check called.")
        result = await crud.inventory_check.delete_inventory_check(self.db, inventory_check_id)
        logger.info("InventoryCheckService: delete_inventory_check called successfully.")
        
        self.db.commit()
        return dict(message_code=AppStatus.DELETED_SUCCESSFULLY.message), obj_del