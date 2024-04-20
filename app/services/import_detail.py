import logging
from typing import Optional
import uuid
from fastapi import HTTPException
from sqlalchemy.orm import Session
from pydantic import UUID4

from app import crud
from app.constant.app_status import AppStatus
from app.models.import_detail import ImportDetail
from app.schemas.import_detail import ImportDetailCreate, ImportDetailCreateParams
from app.schemas.import_detail import ImportDetailCreateParams, ImportDetailCreate, ImportDetailUpdate
from app.core.exceptions import error_exception_handler

logger = logging.getLogger(__name__)

class ImportDetailService:
    def __init__(self, db: Session):
        self.db = db
        
    async def get_all_import_details(
        self,
        tenant_id: str,
        branch: Optional[str] = None,
        limit: Optional[int] = None,
        offset:Optional[int] = None,
        query_search: Optional[str] = None
        ):
        conditions = dict()
        
              
        if conditions:
            whereConditions = await self.whereConditionBuilderForFilter(tenant_id, conditions, branch)
            sql = f"SELECT * FROM public.import_detail {whereConditions};"
            
            if offset is not None and limit is not None:
                sql = f"SELECT * FROM public.import_detail {whereConditions} LIMIT {limit} OFFSET {offset*limit};"

            total = f"SELECT COUNT(*) FROM public.import_detail {whereConditions};"
            
            logger.info("ImportDetailService: filter_import_detail called.")
            result,total = await crud.import_detail.get_import_detail_by_conditions(self.db, sql=sql, total=total)
            total = total[0]['count']
            logger.info("ImportDetailService: filter_import_detail called successfully.")
        elif query_search:
            whereConditions = await self.whereConditionBuilderForSearch(tenant_id, query_search, branch)
            
            sql = f"SELECT * FROM public.import_detail {whereConditions};"
            
            if limit is not None and offset is not None:
                sql = f"SELECT * FROM public.import_detail {whereConditions} LIMIT {limit} OFFSET {offset*limit};"
                
            
            total = f"SELECT COUNT(*) FROM public.import_detail {whereConditions};"

            logger.info("ImportDetailService: filter_import_detail called.")
            result,total= await crud.customer.get_customer_by_conditions(self.db, sql=sql,total = total)
            total = total[0]['count']
        else: 
            logger.info("ImportDetailService: get_all_import_details called.")
            if limit is not None and offset is not None:
                result, total = crud.import_detail.get_multi(db=self.db, skip=offset*limit, limit=limit, tenant_id=tenant_id, branch=branch)
            else: 
                print("successaaa")
                result, total = crud.import_detail.get_multi(db=self.db, tenant_id=tenant_id, branch=branch)
            logger.info("ImportDetailService: get_all_import_details called successfully.")
        
        return dict(message_code=AppStatus.SUCCESS.message,total=total), result
    
    async def get_import_detail_by_id(self, import_detail_id: str):
        logger.info("ImportDetailService: get_import_detail_by_id called.")
        result = await crud.import_detail.get_import_detail_by_id(db=self.db, import_detail_id=import_detail_id)
        logger.info("ImportDetailService: get_import_detail_by_id called successfully.")
        
        return dict(message_code=AppStatus.SUCCESS.message), dict(data=result)
    
    async def gen_id(self):
        newID: str
        lastID = await crud.import_detail.get_last_id(self.db)
        lenID = len(str(lastID))
        if lenID >= 9:
            return str(lastID + 1)
        else:
            newID = str(lastID + 1)
            len_rest = 9 - lenID
    
            for i in range(len_rest):
                newID = '0' + newID
    
            return 'IORDER' + newID
    
    async def create_import_detail(
        self, 
        obj_in: ImportDetailCreateParams,
        user_id:str,
        tenant_id:str,
        db_contract: ImportDetail = None
        ):
        
        newID = await self.gen_id()
        if db_contract:
            import_detail_obj = ImportDetailCreateParams(
                product_id = db_contract.product_id,
                product_name= db_contract.product_name,
                unit= db_contract.unit,
                import_price= db_contract.import_price,
                quantity= db_contract.quantity,
                tenant_id = tenant_id
            )    
            import_detail = crud.import_detail.create(db=self.db, obj_in=import_detail_obj)
        
        import_detail_obj = ImportDetailCreate(
            id=newID,
            is_contract=obj_in.is_contract,
            estimated_date=obj_in.estimated_date,
            delivery_status=obj_in.delivery_status,
            payment_status=obj_in.payment_status,
            subtotal=obj_in.subtotal,
            promotion=obj_in.promotion,
            total=obj_in.total,
            status="Đã nhập hàng" ,
            created_by=user_id,
            belong_to_vendor=obj_in.belong_to_vendor,
            belong_to_contract=obj_in.belong_to_contract,
            tenant_id= tenant_id
        )
        
        
        logger.info("ImportDetailService: create called.")
        result = crud.import_detail.create(db=self.db, obj_in=import_detail_obj)
        logger.info("ImportDetailService: create called successfully.")
        
        self.db.commit()
        logger.info("Service: create_import_detail success.")
        return dict(message_code=AppStatus.SUCCESS.message), import_detail_obj
    
    async def update_import_detail(self, import_detail_id: str, obj_in: ImportDetailUpdate):
        logger.info("ImportDetailService: get_import_detail_by_id called.")
        isValidImportDetail = await crud.import_detail.get_import_detail_by_id(db=self.db, import_detail_id=import_detail_id)
        logger.info("ImportDetailService: get_import_detail_by_id called successfully.")
        
        if not isValidImportDetail:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_IMPORT_ORDER_NOT_FOUND)
        
        logger.info("ImportDetailService: update_import_detail called.")
        result = await crud.import_detail.update_import_detail(db=self.db, import_detail_id=import_detail_id, import_detail_update=obj_in)
        logger.info("ImportDetailService: update_import_detail called successfully.")
        self.db.commit()
        return dict(message_code=AppStatus.UPDATE_SUCCESSFULLY.message), dict(data=result)
        
    async def delete_import_detail(self, import_detail_id: str):
        logger.info("ImportDetailService: get_import_detail_by_id called.")
        isValidImportDetail = await crud.import_detail.get_import_detail_by_id(db=self.db, import_detail_id=import_detail_id)
        logger.info("ImportDetailService: get_import_detail_by_id called successfully.")
        
        if not isValidImportDetail:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_IMPORT_ORDER_NOT_FOUND)
        
        logger.info("ImportDetailService: delete_import_detail called.")
        result = await crud.import_detail.delete_import_detail(self.db, import_detail_id)
        logger.info("ImportDetailService: delete_import_detail called successfully.")
        
        self.db.commit()
        return dict(message_code=AppStatus.DELETED_SUCCESSFULLY.message), dict(data=result)