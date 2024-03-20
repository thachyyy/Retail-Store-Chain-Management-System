import logging
import uuid

from datetime import date
from sqlalchemy.orm import Session
from pydantic import UUID4

from app import crud
from app.constant.app_status import AppStatus
from app.schemas.purchase_order import PurchaseOrderResponse, PurchaseOrderCreate, PurchaseOrderCreateParams
from app.utils import hash_lib
from app.core.exceptions import error_exception_handler
from datetime import datetime
logger = logging.getLogger(__name__)

class PurchaseOrderService:
    def __init__(self, db: Session):
        self.db = db
    
    async def get_purchase_order_by_id(self, purchase_order_id: str):
        logger.info("PurchaseOrderService: get_purchase_order_by_id called.")
        result = await crud.purchase_order.get_purchase_order_by_id(db=self.db, purchase_order_id=purchase_order_id)
        logger.info("PurchaseOrderService: get_purchase_order_by_id called successfully.")
        
        return dict(message_code=AppStatus.SUCCESS.message), dict(data=result)
    
    async def get_all_purchase_orders(self):
        logger.info("PurchaseOrderService: get_all_purchase_orders called.")
        result = await crud.purchase_order.get_all_purchase_orders(db=self.db)
        logger.info("PurchaseOrderService: get_all_purchase_orders called successfully.")
        
        return dict(message_code=AppStatus.SUCCESS.message), dict(data=result)
    
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
    
            return 'PORDER' + newID
        
    async def create_purchase_order(self, obj_in: PurchaseOrderCreateParams, user:str):
        newID = await self.gen_id()
        
        purchase_order_create = PurchaseOrderCreate(
        id=newID,
        created_at=datetime.now(),
        estimated_delivery_date=obj_in.estimated_delivery_date,
        tax=obj_in.tax,
        subtotal=obj_in.subtotal,
        promote=obj_in.promote,
        total=obj_in.total,
        tax_percentage=obj_in.tax_percentage,
        status=obj_in.status,  
        note=obj_in.note,
        handle_by=user,
        belong_to_customer=obj_in.belong_to_customer
    )
        
        logger.info("PurchaseOrderService: create called.")
        result = crud.purchase_order.create(db=self.db, obj_in=purchase_order_create)
        logger.info("PurchaseOrderService: create called successfully.")
        
        self.db.commit()
        logger.info("Service: create_purchase_order success.")
        return dict(message_code=AppStatus.SUCCESS.message), purchase_order_create
    
    async def update_purchase_order(self, purchase_order_id: str, obj_in):
        logger.info("PurchaseOrderService: get_purchase_order_by_id called.")
        isValidPurchaseOrder = await crud.purchase_order.get_purchase_order_by_id(db=self.db, purchase_order_id=purchase_order_id)
        logger.info("PurchaseOrderService: get_purchase_order_by_id called successfully.")
        
        if not isValidPurchaseOrder:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_PURCHASE_NOT_FOUND)
        
        logger.info("PurchaseOrderService: update_purchase_order called.")
        result = await crud.purchase_order.update_purchase_order(db=self.db, purchase_order_id=purchase_order_id, purchase_order_update=obj_in)
        logger.info("PurchaseOrderService: update_purchase_order called successfully.")
        self.db.commit()
        return dict(message_code=AppStatus.UPDATE_SUCCESSFULLY.message), dict(data=result)
        
    async def delete_purchase_order(self, purchase_order_id: str):
        logger.info("PurchaseOrderService: get_purchase_order_by_id called.")
        isValidPurchaseOrder = await crud.purchase_order.get_purchase_order_by_id(db=self.db, purchase_order_id=purchase_order_id)
        logger.info("PurchaseOrderService: get_purchase_order_by_id called successfully.")
        
        if not isValidPurchaseOrder:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_PURCHASE_NOT_FOUND)
        
        logger.info("PurchaseOrderService: delete_purchase_order called.")
        result = await crud.purchase_order.delete_purchase_order(self.db, purchase_order_id)
        logger.info("PurchaseOrderService: delete_purchase_order called successfully.")
        
        self.db.commit()
        return dict(message_code=AppStatus.DELETED_SUCCESSFULLY.message), dict(data=result)
    
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