import logging
import uuid

from sqlalchemy.orm import Session
from pydantic import UUID4

from app import crud
from app.constant.app_status import AppStatus
from app.schemas.product_of_import_order import ProductOfImportOrderCreateParams, ProductOfImportOrderCreate, ProductOfImportOrderUpdate
from app.core.exceptions import error_exception_handler

logger = logging.getLogger(__name__)

class ProductOfImportOrderService:
    def __init__(self, db: Session):
        self.db = db
        
    async def get_all_product_of_import_orders(self):
        logger.info("ProductOfImportOrderService: get_all_product_of_import_orders called.")
        result = await crud.product_of_import_order.get_all_product_of_import_orders(db=self.db)
        logger.info("ProductOfImportOrderService: get_all_product_of_import_orders called successfully.")
        
        return dict(message_code=AppStatus.SUCCESS.message), dict(data=result)
    
    async def get_product_of_import_order_by_id(self, product_of_import_order_id: str):
        logger.info("ProductOfImportOrderService: get_product_of_import_order_by_id called.")
        result = await crud.product_of_import_order.get_product_of_import_order_by_id(db=self.db, product_of_import_order_id=product_of_import_order_id)
        logger.info("ProductOfImportOrderService: get_product_of_import_order_by_id called successfully.")
        
        return dict(message_code=AppStatus.SUCCESS.message), dict(data=result)
    
    async def create_product_of_import_order(self, obj_in: ProductOfImportOrderCreateParams):
        
        
        product_of_import_order_create = ProductOfImportOrderCreate(
            id=uuid.uuid4(),
            product_id=obj_in.product_id,
            import_order_id=obj_in.import_order_id,
            import_price=obj_in.import_price
        )
        
        logger.info("ProductOfImportOrderService: create called.")
        result = crud.product_of_import_order.create(db=self.db, obj_in=product_of_import_order_create)
        logger.info("ProductOfImportOrderService: create called successfully.")
        
        self.db.commit()
        logger.info("Service: create_product_of_import_order success.")
        return dict(message_code=AppStatus.SUCCESS.message), dict(data=product_of_import_order_create)
    
    async def update_product_of_import_order(self, product_of_import_order_id: str, obj_in):
        logger.info("ProductOfImportOrderService: get_product_of_import_order_by_id called.")
        isValidProductOfImportOrder = await crud.product_of_import_order.get_product_of_import_order_by_id(db=self.db, product_of_import_order_id=product_of_import_order_id)
        logger.info("ProductOfImportOrderService: get_product_of_import_order_by_id called successfully.")
        
        if not isValidProductOfImportOrder:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_PRODUCT_OF_IMPORT_ORDER_NOT_FOUND)
        
        logger.info("ProductOfImportOrderService: update_product_of_import_order called.")
        result = await crud.product_of_import_order.update_product_of_import_order(db=self.db, product_of_import_order_id=product_of_import_order_id, product_of_import_order_update=obj_in)
        logger.info("ProductOfImportOrderService: update_product_of_import_order called successfully.")
        self.db.commit()
        return dict(message_code=AppStatus.UPDATE_SUCCESSFULLY.message), dict(data=result)
        
    async def delete_product_of_import_order(self, product_of_import_order_id: str):
        logger.info("ProductOfImportOrderService: get_product_of_import_order_by_id called.")
        isValidProductOfImportOrder = await crud.product_of_import_order.get_product_of_import_order_by_id(db=self.db, product_of_import_order_id=product_of_import_order_id)
        logger.info("ProductOfImportOrderService: get_product_of_import_order_by_id called successfully.")
        
        if not isValidProductOfImportOrder:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_PRODUCT_OF_IMPORT_ORDER_NOT_FOUND)
        
        logger.info("ProductOfImportOrderService: delete_product_of_import_order called.")
        result = await crud.product_of_import_order.delete_product_of_import_order(self.db, product_of_import_order_id)
        logger.info("ProductOfImportOrderService: delete_product_of_import_order called successfully.")
        
        self.db.commit()
        return dict(message_code=AppStatus.DELETED_SUCCESSFULLY.message), dict(data=result)
    