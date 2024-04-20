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
from app.schemas.import_order import ImportOrderCreateParams, ImportOrderCreate, ImportOrderUpdate, InvoiceOrderResponse
from app.core.exceptions import error_exception_handler

logger = logging.getLogger(__name__)

class ImportOrderService:
    def __init__(self, db: Session):
        self.db = db
        
    async def get_all_import_orders(
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
            sql = f"SELECT * FROM public.import_order {whereConditions};"
            
            if offset is not None and limit is not None:
                sql = f"SELECT * FROM public.import_order {whereConditions} LIMIT {limit} OFFSET {offset*limit};"

            total = f"SELECT COUNT(*) FROM public.import_order {whereConditions};"
            
            logger.info("ImportOrderService: filter_import_order called.")
            result,total = await crud.import_order.get_import_order_by_conditions(self.db, sql=sql, total=total)
            total = total[0]['count']
            logger.info("ImportOrderService: filter_import_order called successfully.")
        elif query_search:
            whereConditions = await self.whereConditionBuilderForSearch(tenant_id, query_search, branch)
            
            sql = f"SELECT * FROM public.import_order {whereConditions};"
            
            if limit is not None and offset is not None:
                sql = f"SELECT * FROM public.import_order {whereConditions} LIMIT {limit} OFFSET {offset*limit};"
                
            
            total = f"SELECT COUNT(*) FROM public.import_order {whereConditions};"

            logger.info("ImportOrderService: filter_import_order called.")
            result,total= await crud.customer.get_customer_by_conditions(self.db, sql=sql,total = total)
            total = total[0]['count']
        else: 
            logger.info("ImportOrderService: get_all_import_orders called.")
            if limit is not None and offset is not None:
                result, total = crud.import_order.get_multi(db=self.db, skip=offset*limit, limit=limit, tenant_id=tenant_id, branch=branch)
            else: 
                result, total = crud.import_order.get_multi(db=self.db, tenant_id=tenant_id, branch=branch)
            logger.info("ImportOrderService: get_all_import_orders called successfully.")
            
            response = []
            for x in result:
                r = await self.make_response_import_order(x)
                response.append(r)
        return dict(message_code=AppStatus.SUCCESS.message,total=total), response
    
    async def make_response_import_order(self, obj_in):
        response = InvoiceOrderResponse(
            id=obj_in.id,
            created_at=obj_in.created_at,
            updated_at=obj_in.updated_at,
            is_contract=obj_in.is_contract,
            estimated_date=obj_in.estimated_date,
            delivery_status=obj_in.delivery_status,
            payment_status=obj_in.payment_status,
            subtotal=obj_in.subtotal,
            promotion=obj_in.promotion,
            total=obj_in.total,
            status="Đã nhập hàng",
            created_by= obj_in.created_by,
            belong_to_vendor=obj_in.belong_to_vendor,
            belong_to_contract=obj_in.belong_to_contract,
            tenant_id= obj_in.tenant_id,
            list_import=[]
        )
       
        for id in obj_in.list_import:
            list_import = await crud.import_detail.get_import_detail_by_id(self.db, id)

            response.list_import.append(list_import)

            
            
        return response
    
    async def get_import_order_by_id(self, id: str):
        logger.info("ImportOrderService: get_import_order_by_id called.")
        result = await crud.import_order.get_import_order_by_id(db=self.db, id=id)
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
        user_id:str,
        tenant_id:str,
        
        ):
        
        newID = await self.gen_id()
        # if db_contract:
        #     print("GET db_contract")
        #     import_detail_obj = ImportDetailCreateParams(
        #         product_id = db_contract.product_id,
        #         product_name= db_contract.product_name,
        #         unit= db_contract.unit,
        #         import_price= db_contract.import_price,
        #         quantity= db_contract.quantity,
        #         tenant_id = tenant_id
        #     )    
        #     import_detail = crud.import_detail.create(db=self.db, obj_in=import_detail_obj)
        
        import_order_obj = ImportOrderCreate(
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
            tenant_id= tenant_id,
            list_import=obj_in.list_import,
            branch=obj_in.branch
        )
        
        
        logger.info("ImportOrderService: create called.")
        result = crud.import_order.create(db=self.db, obj_in=import_order_obj)
        logger.info("ImportOrderService: create called successfully.")
        
        self.db.commit()
        logger.info("Service: create_import_order success.")
        return dict(message_code=AppStatus.SUCCESS.message), import_order_obj
    
    async def update_import_order(self,id: str, branch: str, obj_in: ImportOrderUpdate, tenant_id: str):
        logger.info("ImportOrderService: get_import_order_by_id called.")
        isValidImportOrder = await crud.import_order.get_import_order_by_id(db=self.db, id=id, branch=branch, tenant_id=tenant_id)
        logger.info("ImportOrderService: get_import_order_by_id called successfully.")
        
        if not isValidImportOrder:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_IMPORT_ORDER_NOT_FOUND)
        
        logger.info("ImportOrderService: update_import_order called.")
        result = await crud.import_order.update_import_order(db=self.db, id=id, import_order_update=obj_in)
        logger.info("ImportOrderService: update_import_order called successfully.")
        self.db.commit()
        return dict(message_code=AppStatus.UPDATE_SUCCESSFULLY.message), result
        
    async def delete_import_order(self, id: str,tenant_id: str,branch:str):
        logger.info("ImportOrderService: get_import_order_by_id called.")
        isValidImportOrder = await crud.import_order.get_import_order_by_id(db=self.db,id=id,branch=branch,tenant_id=tenant_id)
        logger.info("ImportOrderService: get_import_order_by_id called successfully.")
        
        if not isValidImportOrder:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_IMPORT_ORDER_NOT_FOUND)
        
        logger.info("ImportOrderService: delete_import_order called.")
        result = await crud.import_order.delete_import_order(self.db, id)
        logger.info("ImportOrderService: delete_import_order called successfully.")
        
        self.db.commit()
        return dict(message_code=AppStatus.DELETED_SUCCESSFULLY.message), result