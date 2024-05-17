import logging
from typing import Optional
import uuid
from fastapi import HTTPException
from sqlalchemy.orm import Session
from pydantic import UUID4
from datetime import date, timedelta

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
        offset: Optional[int] = None,
        status: Optional[str] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        query_search: Optional[str] = None
        ):
        conditions = dict()
        
        if status:
            conditions['status'] = status
        if start_date:
            conditions['start_date'] = start_date
        if end_date:
            end_date += timedelta(days=1)
            conditions['end_date'] = end_date
            
        if conditions:
            whereConditions = await self.whereConditionBuilderForFilter(tenant_id, conditions, branch)
            sql = f"SELECT * FROM public.import_order {whereConditions};"
            
            if limit is not None and offset is not None:
                sql = f"SELECT * FROM public.import_order {whereConditions} LIMIT {limit} OFFSET {offset*limit};"
            
            total = f"SELECT COUNT(*) FROM public.import_order {whereConditions};"

            logger.info("InvoiceForCustomerService: filter_import_order called.")
            result,total= await crud.import_order.get_import_order_by_conditions(self.db, sql=sql,total = total)
            total = total[0]['count']
            
        elif query_search:
            whereConditions = await self.whereConditionBuilderForSearch(tenant_id, query_search, branch)
            
            sql = f"SELECT * FROM public.import_order {whereConditions};"
            
            if limit is not None and offset is not None:
                sql = f"SELECT * FROM public.import_order {whereConditions} LIMIT {limit} OFFSET {offset*limit};"
                
            
            total = f"SELECT COUNT(*) FROM public.import_order {whereConditions};"

            logger.info("InvoiceForCustomerService: filter_import_order called.")
            result,total= await crud.import_order.get_import_order_by_conditions(self.db, sql=sql,total = total)
            total = total[0]['count']
        
        else:
            logger.info("ImportOrderService: get_all_import_orders called.")
            if limit is not None and offset is not None:
                result, total = await crud.import_order.get_all_import_orders(db=self.db, offset=offset*limit, limit=limit, tenant_id=tenant_id, branch=branch)
            else: 
                result, total = await crud.import_order.get_all_import_orders(db=self.db, tenant_id=tenant_id, branch=branch)
            logger.info("ImportOrderService: get_all_import_orders called successfully.")
            
        response = []
        for x in result:
            r = await self.make_response_import_order(x)
            response.append(r)
        return dict(message_code=AppStatus.SUCCESS.message,total=total), response
    
    async def make_response_import_order(self, obj_in):
        vendor_name = await crud.import_detail.get_vendor_name(self.db, obj_in.belong_to_vendor)
        response = InvoiceOrderResponse(
            id=obj_in.id,
            created_at=obj_in.created_at,
            updated_at=obj_in.updated_at,
            is_contract=obj_in.is_contract,
            estimated_date=obj_in.estimated_date,
            payment_status=obj_in.payment_status,
            total=obj_in.total,
            status="Đã nhập hàng",
            created_by= obj_in.created_by,
            belong_to_vendor=obj_in.belong_to_vendor,
            vendor_name=vendor_name,
            belong_to_contract=obj_in.belong_to_contract,
            tenant_id= obj_in.tenant_id,
            list_import=[],
            branch= obj_in.branch
        )
       
        for id in obj_in.list_import:
            list_import = await crud.import_detail.get_import_detail_by_id(self.db, id)
            response.list_import.append(list_import)

        return response
    
    async def get_import_order_by_id(self, id: str, tenant_id: str, branch: str):
        logger.info("ImportOrderService: get_import_order_by_id called.")
        result = await crud.import_order.get_import_order_by_id(db=self.db, id=id, branch=branch, tenant_id=tenant_id)
        logger.info("ImportOrderService: get_import_order_by_id called successfully.")
        
        r = await self.make_response_import_order(result)
        return dict(message_code=AppStatus.SUCCESS.message), r
        
        # return dict(message_code=AppStatus.SUCCESS.message), dict(data=result)
    
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
        
        import_order_obj = ImportOrderCreate(
            id=newID,
            is_contract=obj_in.is_contract,
            estimated_date=obj_in.estimated_date,
            payment_status=obj_in.payment_status,
            total=obj_in.total,
            status="Đã nhập hàng" ,
            created_by=user_id,
            belong_to_vendor=obj_in.belong_to_vendor,
            belong_to_contract=obj_in.belong_to_contract,
            tenant_id= tenant_id,
            branch=obj_in.branch,
            list_import=obj_in.list_import
        )
        
        if obj_in.is_contract == True:
            period = await crud.import_order.get_period_contract(db=self.db, id=obj_in.belong_to_contract)
            if period != None:
                latest_import = date.today()
                next_import = latest_import + timedelta(days=int(period))
                await crud.import_order.update_date_import(db=self.db, id=obj_in.belong_to_contract, latest_import=latest_import, next_import=next_import)
        
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
    
    async def whereConditionBuilderForFilter(self, tenant_id: str, conditions: dict, branch: str = None) -> str:
        whereList = list()
        whereList.append(f"tenant_id = '{tenant_id}'")
        
        if branch is not None:
            whereList.append(f"branch = '{branch}'")
            
        if 'status' in conditions:
            whereList.append(f"LOWER(status) = LOWER('{conditions['status']}')")
        if 'start_date' in conditions:
            whereList.append(f"created_at >= '{conditions['start_date']}'")
        if 'end_date' in conditions:
            whereList.append(f"created_at <= '{conditions['end_date']}'")
            
        whereConditions = "WHERE " + ' AND '.join(whereList)
        return whereConditions
    
    async def whereConditionBuilderForSearch(self, tenant_id: str, condition: str, branch: str = None) -> str:
        conditions = list()
        conditions.append(f"id::text ilike '%{condition}%'")
        
        whereCondition = ' OR '.join(conditions)
        if branch is not None:
            whereCondition = f"WHERE ({whereCondition}) AND tenant_id = '{tenant_id}' AND branch = '{branch}'"
        else:
            whereCondition = f"WHERE ({whereCondition}) AND tenant_id = '{tenant_id}'"
        return whereCondition