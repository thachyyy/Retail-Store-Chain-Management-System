import logging
from typing import Optional
import uuid
import math

from datetime import date
from sqlalchemy.orm import Session
from pydantic import UUID4, Field

from app import crud
from app.api.endpoints.batch import update_batch
from app.api.endpoints.invoice_for_customer import create_invoice_for_customer
from app.constant.app_status import AppStatus
from app.models.employee import Employee
from app.schemas.invoice_for_customer import InvoiceForCustomerCreateParams
from app.schemas.order_detail import OrderDetails
from app.schemas.purchase_order import PurchaseOrderResponse, PurchaseOrderCreate, PurchaseOrderCreateParams
from app.utils import hash_lib
from app.core.exceptions import error_exception_handler
from datetime import datetime
logger = logging.getLogger(__name__)

class PurchaseOrderService:
    def __init__(self, db: Session):
        self.db = db
    
    async def get_purchase_order_by_id(self, purchase_order_id: str, tenant_id: str):
        logger.info("PurchaseOrderService: get_purchase_order_by_id called.")
        result = await crud.purchase_order.get_purchase_order_by_id(db=self.db, purchase_order_id=purchase_order_id, tenant_id=tenant_id)
        
        order_detail = await crud.purchase_order.get_order_detail(self.db, result[0].id)
        setattr(result[0], "order_details", order_detail)
        
        logger.info("PurchaseOrderService: get_purchase_order_by_id called successfully.")
        
        return dict(message_code=AppStatus.SUCCESS.message), result[0]
   
    async def get_all_purchase_orders(
        self, 
        tenant_id: str,
        branch: Optional[str],
        limit: Optional[int] = None,
        offset:Optional[int] = None,
        status:Optional[str] = None,
        handle_by:Optional[str] = None,
        gt_total:Optional[int] = None,
        lt_total:Optional[int] = None,
        start_date:Optional[date] = None,
        end_date:Optional[date] = None,
        query_search:Optional[str] = None
    ):
        
        conditions = dict()
        if status:
            conditions['status'] = status
        if gt_total:
            conditions['gt_total'] = gt_total
        if lt_total:
            conditions['lt_total'] = lt_total
        if start_date:
            conditions['start_date'] = start_date
        if end_date:
            conditions['end_date'] = end_date
        if handle_by:
            conditions['handle_by'] = handle_by
        
        
        if conditions:
            whereConditions = await self.whereConditionBuilderForFilter(tenant_id, conditions, branch)
            sql = f"SELECT * FROM public.purchase_order {whereConditions};"
            
            if offset is not None and limit is not None:
                sql = f"SELECT * FROM public.purchase_order {whereConditions} LIMIT {limit} OFFSET {offset*limit};"
                
            total = f"SELECT COUNT(*) FROM public.purchase_order {whereConditions};"

            logger.info("PurchaseOrderService: filter_purchase_order called.")
            result,total= await crud.purchase_order.get_purchase_order_by_conditions(self.db, sql=sql,total = total)
            total = total[0]['count']
            logger.info("PurchaseOrderService: filter_purchase_order called successfully.")
            
        elif query_search:
            whereConditions = await self.whereConditionBuilderForSearch(tenant_id, query_search, branch)
            
            sql = f"SELECT * FROM public.purchase_order {whereConditions};"
            
            if limit is not None and offset is not None:
                sql = f"SELECT * FROM public.purchase_order {whereConditions} LIMIT {limit} OFFSET {offset*limit};"
                
            
            total = f"SELECT COUNT(*) FROM public.purchase_order {whereConditions};"

            logger.info("PurchaseOrderService: filter_purchase_order called.")
            result,total= await crud.purchase_order.get_purchase_order_by_conditions(self.db, sql=sql,total = total)
            total = total[0]['count']
        else: 
            sql = f"SELECT COUNT(*) FROM public.purchase_order WHERE tenant_id = '{tenant_id}' AND branch = '{branch}';"
            logger.info("PurchaseOrderService: get_all_purchase_order called.")
            if limit is not None and offset is not None:
                result, total = await crud.purchase_order.get_all_purchase_orders(db=self.db,sql=sql,tenant_id=tenant_id,branch=branch, offset=offset*limit,limit=limit)
                total = total[0]['count']
            else: 
                result, total = await crud.purchase_order.get_all_purchase_orders(db=self.db,sql=sql,tenant_id=tenant_id,branch=branch)
                total = total[0]['count']
            logger.info("PurchaseOrderService: get_all_purchase_order called successfully.")

        response = []
        for x in result:
            order_detail = await crud.purchase_order.get_order_detail(self.db, x.id)
            setattr(x, "order_details", order_detail)
            response.append(x)
            
        return dict(message_code=AppStatus.SUCCESS.message,total=total), response
    
    async def whereConditionBuilderForSearch(self, tenant_id: str, condition: str, branch: str = None) -> str:
        conditions = list()
        conditions.append(f"handle_by ilike '%{condition}%'")
        conditions.append(f"belong_to_customer ilike '%{condition}%'")
        
        whereCondition = ' OR '.join(conditions)
        if branch is not None:
            whereCondition = f"WHERE ({whereCondition}) AND tenant_id = '{tenant_id}' AND branch = '{branch}'"
        else:
            whereCondition = f"WHERE ({whereCondition}) AND tenant_id = '{tenant_id}'"
        return whereCondition
    
    async def whereConditionBuilderForFilter(self, tenant_id: str, conditions: dict, branch: str = None) -> str:
        whereList = list()
        whereList.append(f"tenant_id = '{tenant_id}'")
        if branch is not None:
            whereList.append(f"branch = '{branch}'")
        
        # filter using '='
        if 'status' in conditions:
            whereList.append(f"LOWER(status) = LOWER('{conditions['status']}')")
        if 'handle_by' in conditions:
            whereList.append(f"LOWER(handle_by) = LOWER('{conditions['handle_by']}')")
        if 'gt_total' in conditions:
            whereList.append(f"total >= '{conditions['gt_total']}'")
        if 'lt_total' in conditions:
            whereList.append(f"total <= '{conditions['lt_total']}'")
        if 'start_date' in conditions:
            whereList.append(f"created_at >= '{conditions['start_date']}'")
        if 'end_date' in conditions:
            whereList.append(f"created_at <= '{conditions['end_date']}'")
         
        whereConditions = "WHERE " + ' AND '.join(whereList)
        return whereConditions
    async def gen_id(self):
        newID: str
        lastID = await crud.purchase_order.get_last_id(self.db)
        lenID = len(str(lastID))
        if lenID >= 9:
            return str(lastID + 1)
        else:
            newID = str(lastID + 1)
            len_rest = 9 - lenID
    
            for i in range(len_rest):
                newID = '0' + newID
    
            return 'ORDER' + newID
        
    async def create_purchase_order(self, 
                                    obj_in: PurchaseOrderCreateParams,
                                    paid: bool,
                                    user_id:str,
                                    tenant_id:str,
                                    branch:str):
        newID = await self.gen_id()
        status = "Đã thanh toán" if paid else "Đang chờ xử lí"

        # Update batches if paid
        if paid:
            for item in obj_in.order_detail:
                await update_batch(item.batch, item.quantity,tenant_id, db=self.db)
                
        purchase_order_create = PurchaseOrderCreate(
        id=newID,
        estimated_delivery_date=obj_in.estimated_delivery_date,
        tax=obj_in.tax,
        subtotal=obj_in.subtotal,
        promote=obj_in.promote,
        total=obj_in.total,
        tax_percentage=obj_in.tax_percentage,
        status=status,  
        note=obj_in.note,
        handle_by=user_id,
        belong_to_customer=obj_in.belong_to_customer,
        tenant_id =tenant_id,
        branch=branch
        )
        
        logger.info("PurchaseOrderService: create called.")
        result = await crud.purchase_order.create(db=self.db,
                                                  paid=paid,
                                                  obj_in=purchase_order_create,
                                                  obj=obj_in.order_detail,
                                                  tenant_id=tenant_id)
        
        logger.info("PurchaseOrderService: create called successfully.")
        
        self.db.commit()
        
        if obj_in.belong_to_customer:
            current_reward_point = await crud.purchase_order.get_current_reward_point(self.db, obj_in.belong_to_customer)
            print("herrrr", obj_in.reward_point_used)
            print(type(obj_in.reward_point_used))
            if obj_in.reward_point_used:
                if obj_in.reward_point_used > 0 and obj_in.reward_point_used <= current_reward_point:
                    new_reward_point = current_reward_point - obj_in.reward_point_used
                    if new_reward_point < 0:
                        raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_NOT_ENOUGH_POINT)
                    await crud.purchase_order.update_reward_point(self.db, obj_in.belong_to_customer, new_reward_point)
            if not obj_in.reward_point_used:
                reward_point = math.floor(obj_in.total*0.01)
                await crud.purchase_order.update_reward_point(self.db, obj_in.belong_to_customer, reward_point)
        
        logger.info("Service: create_purchase_order success.")
        return dict(message_code=AppStatus.SUCCESS.message), purchase_order_create

    async def update_purchase_order(self, purchase_order_id: str, obj_in, tenant_id: str):
        logger.info("PurchaseOrderService: get_purchase_order_by_id called.")
        isValidPurchaseOrder = await crud.purchase_order.get_purchase_order_by_id(db=self.db, purchase_order_id=purchase_order_id, tenant_id=tenant_id)
        logger.info("PurchaseOrderService: get_purchase_order_by_id called successfully.")
        
        if not isValidPurchaseOrder:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_PURCHASE_NOT_FOUND)
        
        logger.info("PurchaseOrderService: update_purchase_order called.")
        result = await crud.purchase_order.update_purchase_order(db=self.db, purchase_order_id=purchase_order_id, purchase_order_update=obj_in)
        logger.info("PurchaseOrderService: update_purchase_order called successfully.")
        self.db.commit()
        return dict(message_code=AppStatus.UPDATE_SUCCESSFULLY.message), result
        
    async def delete_purchase_order(self, purchase_order_id: str, tenant_id: str):
        logger.info("PurchaseOrderService: get_purchase_order_by_id called.")
        isValidPurchaseOrder = await crud.purchase_order.get_purchase_order_by_id(db=self.db, purchase_order_id=purchase_order_id, tenant_id=tenant_id)
        logger.info("PurchaseOrderService: get_purchase_order_by_id called successfully.")
        
        if not isValidPurchaseOrder:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_PURCHASE_NOT_FOUND)
        
        logger.info("PurchaseOrderService: delete_purchase_order called.")
        result = await crud.purchase_order.delete_purchase_order(self.db, purchase_order_id)
        logger.info("PurchaseOrderService: delete_purchase_order called successfully.")
        
        self.db.commit()
        return dict(message_code=AppStatus.DELETED_SUCCESSFULLY.message), result
    
    # async def whereConditionBuilderForSearch(self, condition: str) -> str:
    #     conditions = list()
    #     conditions.append(f"id::text ilike '%{condition}%'")
    #     conditions.append(f"full_name ilike '%{condition}%'")
    #     conditions.append(f"phone_number ilike '%{condition}%'")
    #     conditions.append(f"address ilike '%{condition}%'")
            
    #     whereCondition = "WHERE " + ' OR '.join(conditions)
    #     return whereCondition
    
#     async def whereConditionBuilderForFilter(self, conditions: dict) -> str:
#         whereList = list()
        
#         if 'gender' in conditions:
#             whereList.append(f"gender = '{conditions['gender']}'")
#         if 'province' in conditions:
#             whereList.append(f"province = '{conditions['province']}'")
#         if 'district' in conditions:
#             whereList.append(f"district = '{conditions['district']}'")
#         if 'start_date' in conditions and 'end_date' in conditions:
#             whereList.append(f"dob between '{conditions['start_date']}' and '{conditions['end_date']}'")
            
#         whereConditions = "WHERE " + ' AND '.join(whereList)
#         return whereConditions
    
#     async def search_purchase_order(self, condition: str = None):
#         whereCondition = await self.whereConditionBuilderForSearch(condition)
#         sql = f"SELECT * FROM public.purchase_order {whereCondition};"
        
#         logger.info("PurchaseOrderService: search_purchase_order called.")
#         result = await crud.purchase_order.search_purchase_order(self.db, sql)
#         logger.info("PurchaseOrderService: search_purchase_order called successfully.")
        
#         return dict(message_code=AppStatus.SUCCESS.message), dict(data=result)
    
#     async def filter_purchase_order(
#         self,
#         gender: str = None,
#         start_date: date = None,
#         end_date: date = None,
#         province: str = None,
#         district: str = None,
# ):
#         conditions = dict()
#         if gender:
#             conditions['gender'] = gender
#         if start_date:
#             conditions['start_date'] = start_date
#         if end_date:
#             conditions['end_date'] = end_date
#         if province:
#             conditions['province'] = province
#         if district:
#             conditions['district'] = district
        
#         whereConditions = await self.whereConditionBuilderForFilter(conditions)
#         sql = f"SELECT * FROM public.purchase_order {whereConditions};"
        
#         logger.info("PurchaseOrderService: filter_purchase_order called.")
#         result = await crud.purchase_order.filter_purchase_order(self.db, sql)
#         logger.info("PurchaseOrderService: filter_purchase_order called successfully.")
        
#         return dict(message_code=AppStatus.SUCCESS.message), dict(data=result)