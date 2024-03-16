import logging
import uuid

from sqlalchemy.orm import Session
from pydantic import UUID4

from app import crud
from app.constant.app_status import AppStatus
from app.schemas.order_of_batch import OrderOfBatchCreateParams, OrderOfBatchCreate, OrderOfBatchUpdate
from app.core.exceptions import error_exception_handler

logger = logging.getLogger(__name__)

class OrderOfBatchService:
    def __init__(self, db: Session):
        self.db = db
        
    async def get_all_order_of_batches(self):
        logger.info("OrderOfBatchService: get_all_order_of_batches called.")
        result = await crud.order_of_batch.get_all_order_of_batches(db=self.db)
        logger.info("OrderOfBatchService: get_all_order_of_batches called successfully.")
        
        return dict(message_code=AppStatus.SUCCESS.message), dict(data=result)
    
    async def get_order_of_batch_by_id(self, order_of_batch_id: str):
        logger.info("OrderOfBatchService: get_order_of_batch_by_id called.")
        result = await crud.order_of_batch.get_order_of_batch_by_id(db=self.db, order_of_batch_id=order_of_batch_id)
        logger.info("OrderOfBatchService: get_order_of_batch_by_id called successfully.")
        
        return dict(message_code=AppStatus.SUCCESS.message), dict(data=result)
    
    async def create_order_of_batch(self, obj_in: OrderOfBatchCreateParams):
        
        order_of_batch_create = OrderOfBatchCreate(
            id=uuid.uuid4(),
            price=obj_in.price,
            quantity=obj_in.quantity,
            purchase_order_id=obj_in.purchase_order_id,
            batch_id=obj_in.batch_id
        )
        
        logger.info("OrderOfBatchService: create called.")
        result = crud.order_of_batch.create(db=self.db, obj_in=order_of_batch_create)
        logger.info("OrderOfBatchService: create called successfully.")
        
        self.db.commit()
        logger.info("Service: create_order_of_batch success.")
        return dict(message_code=AppStatus.SUCCESS.message), dict(data=order_of_batch_create)
    
    async def update_order_of_batch(self, order_of_batch_id: str, obj_in):
        logger.info("OrderOfBatchService: get_order_of_batch_by_id called.")
        isValidOrderOfBatch = await crud.order_of_batch.get_order_of_batch_by_id(db=self.db, order_of_batch_id=order_of_batch_id)
        logger.info("OrderOfBatchService: get_order_of_batch_by_id called successfully.")
        
        if not isValidOrderOfBatch:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_ORDER_OF_BATCH_NOT_FOUND)
        
        logger.info("OrderOfBatchService: update_order_of_batch called.")
        result = await crud.order_of_batch.update_order_of_batch(db=self.db, order_of_batch_id=order_of_batch_id, order_of_batch_update=obj_in)
        logger.info("OrderOfBatchService: update_order_of_batch called successfully.")
        self.db.commit()
        return dict(message_code=AppStatus.UPDATE_SUCCESSFULLY.message), dict(data=result)
        
    async def delete_order_of_batch(self, order_of_batch_id: str):
        logger.info("OrderOfBatchService: get_order_of_batch_by_id called.")
        isValidOrderOfBatch = await crud.order_of_batch.get_order_of_batch_by_id(db=self.db, order_of_batch_id=order_of_batch_id)
        logger.info("OrderOfBatchService: get_order_of_batch_by_id called successfully.")
        
        if not isValidOrderOfBatch:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_ORDER_OF_BATCH_NOT_FOUND)
        
        logger.info("OrderOfBatchService: delete_order_of_batch called.")
        result = await crud.order_of_batch.delete_order_of_batch(self.db, order_of_batch_id)
        logger.info("OrderOfBatchService: delete_order_of_batch called successfully.")
        
        self.db.commit()
        return dict(message_code=AppStatus.DELETED_SUCCESSFULLY.message), dict(data=result)
    