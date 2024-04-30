import logging
import uuid
from typing import Optional

from sqlalchemy.orm import Session
from pydantic import UUID4

from app import crud
from app.constant.app_status import AppStatus
from app.schemas.batch import BatchCreateParams, BatchCreate, BatchUpdate
from app.core.exceptions import error_exception_handler
from datetime import datetime

logger = logging.getLogger(__name__)

class BatchService:
    def __init__(self, db: Session):
        self.db = db
        
    async def get_all_batches(
        self,
        tenant_id: str,
        branch: str,
        limit: Optional[int] = None,
        offset:Optional[int] = None,
        query_search : Optional[str] = None):
        logger.info("BatchService: get_all_batches called.")
        
        if query_search:
            whereConditions = await self.whereConditionBuilderForSearch(tenant_id, query_search,branch)
            
            # list newest batch to oldest batch
            sql = f"SELECT * FROM public.batch {whereConditions} ORDER BY created_at DESC;"
            
            if limit is not None and offset is not None:
                sql = f"SELECT * FROM public.batch {whereConditions} LIMIT {limit} OFFSET {offset*limit} ;"
                
            
            total = f"SELECT COUNT(*) FROM public.batch {whereConditions};"

            logger.info("BatchService: filter_batch called.")
            result,total= await crud.batch.get_batch_by_conditions(self.db, sql=sql,total = total)
            total = total[0]['count']
        else:
            if limit is not None and offset is not None:
                result, total = crud.batch.get_multi(db=self.db, skip=offset*limit,limit=limit,tenant_id=tenant_id,branch=branch)
            else: 
                result, total = crud.batch.get_multi(db=self.db,tenant_id=tenant_id,branch=branch)
            logger.info("BatchService: get_all_batches called successfully.")
            
        return dict(message_code=AppStatus.SUCCESS.message, total=total), result
    
    async def get_batch_by_id(self, batch_id: str, tenant_id: str):
        logger.info("BatchService: get_batch_by_id called.")
        result = await crud.batch.get_batch_by_id(db=self.db, batch_id=batch_id, tenant_id=tenant_id)
        logger.info("BatchService: get_batch_by_id called successfully.")
        
        return dict(message_code=AppStatus.SUCCESS.message), result
    
    async def get_batch_by_product_id(self, product_id: str, tenant_id: str):
        logger.info("BatchService: get_batch_by_prod_id called.")
        result = await crud.batch.get_batch_by_product_id(db=self.db, product_id=product_id, tenant_id=tenant_id)
        logger.info("BatchService: get_batch_by_prod_id called successfully.")
        
        return dict(message_code=AppStatus.SUCCESS.message), result
    
    async def gen_id(self):
        newID: str
        lastID = await crud.batch.get_last_id(self.db)
        lenID = len(str(lastID))
        if lenID >= 9:
            return str(lastID + 1)
        else:
            newID = str(lastID + 1)
            len_rest = 9 - lenID
    
            for i in range(len_rest):
                newID = '0' + newID
    
            return 'LO' + newID
    
    async def create_batch(self, obj_in: BatchCreateParams, tenant_id: str, branch: str):
        
        newID = await self.gen_id()
        
        batch_create = BatchCreate(
            id=newID,
            quantity=obj_in.quantity,
            import_price=obj_in.import_price,
            manufacturing_date=obj_in.manufacturing_date,
            expiry_date=obj_in.expiry_date,
            branch=branch,
            belong_to_receipt=obj_in.belong_to_receipt,
            product_id=obj_in.product_id,
            status=0,
            tenant_id=tenant_id
        )
        
        logger.info("BatchService: create called.")
        result = crud.batch.create(db=self.db, obj_in=batch_create)
        logger.info("BatchService: create called successfully.")
        
        self.db.commit()
        logger.info("Service: create_batch success.")
        return dict(message_code=AppStatus.SUCCESS.message), batch_create
    
    async def update_batch(self, batch_id: str, obj_in, tenant_id: str):
        logger.info("BatchService: get_batch_by_id called.")
        isValidBatch = await crud.batch.get_batch_by_id(db=self.db, batch_id=batch_id, tenant_id=tenant_id)
        logger.info("BatchService: get_batch_by_id called successfully.")
        
        if not isValidBatch:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_BATCH_NOT_FOUND)
        
        logger.info("BatchService: update_batch called.")
        result = await crud.batch.update_batch(db=self.db, batch_id=batch_id, batch_update=obj_in, tenant_id=tenant_id)
        logger.info("BatchService: update_batch called successfully.")
        self.db.commit()
        obj_update = await crud.batch.get_batch_by_id(self.db, batch_id, tenant_id)
        return dict(message_code=AppStatus.UPDATE_SUCCESSFULLY.message), obj_update
    
    async def update_quantity(self, batch_id: str, quantity:int,tenant_id:str):
        logger.info("BatchService: get_batch_by_id called.")
        isValidBatch = await crud.batch.get_batch_by_id(db=self.db, batch_id=batch_id,tenant_id=tenant_id)
        logger.info("BatchService: get_batch_by_id called successfully.")
        
        
        if not isValidBatch:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_BATCH_NOT_FOUND)

        logger.info("BatchService: update_batch called.")
        result = await crud.batch.update_quantity(db=self.db, batch_id=batch_id, quantity=quantity,tenant_id=tenant_id)
        logger.info("BatchService: update_batch called successfully.")
        self.db.commit()
        obj_update = await crud.batch.get_batch_by_id(self.db, batch_id,tenant_id)
        return dict(message_code=AppStatus.UPDATE_SUCCESSFULLY.message), obj_update    
    async def delete_batch(self, tenant_id: str, batch_id: str):
        logger.info("BatchService: get_batch_by_id called.")
        isValidBatch = await crud.batch.get_batch_by_id(db=self.db, batch_id=batch_id, tenant_id=tenant_id)
        logger.info("BatchService: get_batch_by_id called successfully.")
        
        if not isValidBatch:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_BATCH_NOT_FOUND)
        
        obj_del = await crud.batch.get_batch_by_id(self.db, batch_id)
        
        logger.info("BatchService: delete_batch called.")
        result = await crud.batch.delete_batch(self.db, batch_id)
        logger.info("BatchService: delete_batch called successfully.")
        
        self.db.commit()
        return dict(message_code=AppStatus.DELETED_SUCCESSFULLY.message), obj_del
    
    async def whereConditionBuilderForSearch(self, tenant_id: str, condition: str, branch: str = None) -> str:
        conditions = list()
        conditions.append(f"id::text ilike '%{condition}%'")
        conditions.append(f"product_id::text ilike '%{condition}%'")
        conditions.append(f"created_at::text ilike '%{condition}%'")
        # conditions.append(f"product_name ilike '%{condition}%'")
        whereCondition = ' OR '.join(conditions)
            
        if branch is not None:
            whereCondition = f"WHERE ({whereCondition}) AND tenant_id = '{tenant_id}' AND branch = '{branch}'"
        else:
            whereCondition = f"WHERE ({whereCondition}) AND tenant_id = '{tenant_id}'"
        return whereCondition