import logging
import uuid
from fastapi import HTTPException
from sqlalchemy.orm import Session
from pydantic import UUID4

from app import crud
from app.constant.app_status import AppStatus
from app.models.import_detail import ImportDetail
from app.schemas.import_detail import ImportDetailCreate
from app.schemas.import_order import ImportOrderCreateParams, ImportOrderCreate, ImportOrderUpdate
from app.core.exceptions import error_exception_handler

logger = logging.getLogger(__name__)

class ImportOrderService:
    def __init__(self, db: Session):
        self.db = db
        
    async def get_all_import_orders(self):
        logger.info("ImportOrderService: get_all_import_orders called.")
        result = await crud.import_order.get_all_import_orders(db=self.db)
        logger.info("ImportOrderService: get_all_import_orders called successfully.")
        
        return dict(message_code=AppStatus.SUCCESS.message), result
    
    async def get_import_order_by_id(self, import_order_id: str):
        logger.info("ImportOrderService: get_import_order_by_id called.")
        result = await crud.import_order.get_import_order_by_id(db=self.db, import_order_id=import_order_id)
        logger.info("ImportOrderService: get_import_order_by_id called successfully.")
        
        return dict(message_code=AppStatus.SUCCESS.message), dict(data=result)
    
    async def gen_id(self):
        newID: str
        lastID = await crud.import_order.get_last_id(self.db)
        lenID = len(str(lastID))
        if lenID >= 9:
            return str(lastID + 1)
        else:
            newID = str(lastID + 1)
            len_rest = 9 - lenID
    
            for i in range(len_rest):
                newID = '0' + newID
    
            return 'IORDER' + newID
    
    async def create_import_order(
        self, 
        obj_in: ImportOrderCreateParams,
        user_name:str,
        tenant_id:str,
        db_contract: ImportDetail
        ):
        
        newID = await self.gen_id()
        import_order_create = ImportDetailCreate(
            product_id = db_contract.product_id,
            product_name= db_contract.product_name,
            unit= db_contract.unit,
            import_price= db_contract.import_price,
            quantity= db_contract.quantity,
            tenant_id = tenant_id
        )    
        import_detail = crud.import_detail.create(db=self.db, obj_in=import_order_create)
        
        import_order_create = ImportOrderCreate(
            id=newID,
            is_contract=obj_in.is_contract,
            estimated_date=obj_in.estimated_date,
            delivery_status=obj_in.delivery_status,
            payment_status=obj_in.payment_status,
            subtotal=obj_in.subtotal,
            promotion=obj_in.promotion,
            total=obj_in.total,
            created_by=user_name,
            belong_to_vendor=obj_in.belong_to_vendor,
            belong_to_contract=obj_in.belong_to_contract,
            tenant_id= tenant_id
        )
        
        
        logger.info("ImportOrderService: create called.")
        result = crud.import_order.create(db=self.db, obj_in=import_order_create)
        logger.info("ImportOrderService: create called successfully.")
        
        self.db.commit()
        logger.info("Service: create_import_order success.")
        return dict(message_code=AppStatus.SUCCESS.message), import_order_create
    
    async def update_import_order(self, import_order_id: str, obj_in: ImportOrderUpdate):
        logger.info("ImportOrderService: get_import_order_by_id called.")
        isValidImportOrder = await crud.import_order.get_import_order_by_id(db=self.db, import_order_id=import_order_id)
        logger.info("ImportOrderService: get_import_order_by_id called successfully.")
        
        if not isValidImportOrder:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_IMPORT_ORDER_NOT_FOUND)
        
        logger.info("ImportOrderService: update_import_order called.")
        result = await crud.import_order.update_import_order(db=self.db, import_order_id=import_order_id, import_order_update=obj_in)
        logger.info("ImportOrderService: update_import_order called successfully.")
        self.db.commit()
        return dict(message_code=AppStatus.UPDATE_SUCCESSFULLY.message), dict(data=result)
        
    async def delete_import_order(self, import_order_id: str):
        logger.info("ImportOrderService: get_import_order_by_id called.")
        isValidImportOrder = await crud.import_order.get_import_order_by_id(db=self.db, import_order_id=import_order_id)
        logger.info("ImportOrderService: get_import_order_by_id called successfully.")
        
        if not isValidImportOrder:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_IMPORT_ORDER_NOT_FOUND)
        
        logger.info("ImportOrderService: delete_import_order called.")
        result = await crud.import_order.delete_import_order(self.db, import_order_id)
        logger.info("ImportOrderService: delete_import_order called successfully.")
        
        self.db.commit()
        return dict(message_code=AppStatus.DELETED_SUCCESSFULLY.message), dict(data=result)