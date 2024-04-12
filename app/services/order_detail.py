import logging
from typing import Optional
import uuid

from datetime import date
from sqlalchemy.orm import Session
from pydantic import UUID4, Field

from app import crud
from app.constant.app_status import AppStatus
# from app.schemas.order_detail import OrderDetailResponse, OrderDetailCreate, OrderDetailCreateParams
from app.utils import hash_lib
from app.core.exceptions import error_exception_handler
from datetime import datetime
logger = logging.getLogger(__name__)

class OrderDetailService:
    def __init__(self, db: Session):
        self.db = db
    
    async def get_order_detail_by_id(self, order_detail_id: str):
        logger.info("OrderDetailService: get_order_detail_by_id called.")
        result = await crud.order_detail.get_order_detail_by_id(db=self.db, order_detail_id=order_detail_id)
        logger.info("OrderDetailService: get_order_detail_by_id called successfully.")
        
        return dict(message_code=AppStatus.SUCCESS.message), result
   

   
    async def get_all_order_details(self, 
        limit: Optional[int] = None,
        offset:Optional[int] = None,
        #  address: str = None,
        # note: str = None,
        # branch_name: str = None,
        query_search: Optional[str] = None 
        ):
        conditions = dict()
        # if role:
        #     conditions['role'] = role
        # if status:
        #     conditions['status'] = status
        # if province:
        #     conditions['province'] = province
        
        
        if conditions:
            whereConditions = await self.whereConditionBuilderForFilter(conditions)
            sql = f"SELECT * FROM public.order_detail {whereConditions};"
            
            if offset is not None and limit is not None:
                sql = f"SELECT * FROM public.order_detail {whereConditions} LIMIT {limit} OFFSET {offset*limit};"
                
            total = f"SELECT COUNT(*) FROM public.order_detail {whereConditions};"

            logger.info("OrderDetailService: filter_order_detail called.")
            result,total= await crud.order_detail.get_order_detail_by_conditions(self.db, sql=sql,total = total)
            total = total[0]['count']
            logger.info("OrderDetailService: filter_order_detail called successfully.")
            
        elif query_search:
            whereConditions = await self.whereConditionBuilderForSearch(query_search)
            
            sql = f"SELECT * FROM public.order {whereConditions};"
            
            if limit is not None and offset is not None:
                sql = f"SELECT * FROM public.order {whereConditions} LIMIT {limit} OFFSET {offset*limit};"
                
            
            total = f"SELECT COUNT(*) FROM public.order {whereConditions};"

            logger.info("OrderDetailService: filter_order_detail called.")
            result,total= await crud.order_detail.get_order_detail_by_conditions(self.db, sql=sql,total = total)
            total = total[0]['count']
        else: 
            sql = f"SELECT COUNT(*) FROM public.order;"
            logger.info("OrderDetailService: get_all_order_details called.")
            if limit is not None and offset is not None:
                result, total = await crud.order_detail.get_all_order_details(db=self.db,sql=sql, offset=offset*limit,limit=limit)
            else: result, total = await crud.order_detail.get_all_order_details(db=self.db,sql=sql)
            logger.info("OrderDetailService: get_all_order_details called successfully.")
            total = total[0]['count']

        
        return dict(message_code=AppStatus.SUCCESS.message,total=total), result
    async def whereConditionBuilderForSearch(self, condition: str) -> str:
        conditions = list()
        conditions.append(f"id::text ilike '%{condition}%'")
        conditions.append(f"full_name::text ilike '%{condition}%'")
    
    async def whereConditionBuilderForFilter(self, conditions: dict) -> str:
        whereList = list()
        
        # filter using '='
        if 'role' in conditions:
            whereList.append(f"role = '{conditions['role']}'")
        if 'status' in conditions:
            whereList.append(f"status = '{conditions['status']}'")
        
        # filter using 'ilike'
        if 'id' in conditions:
            whereList.append(f"id ilike '%{conditions['id']}%'")
        if 'full_name' in conditions:
            whereList.append(f"full_name ilike '%{conditions['full_name']}%'")
        if 'email' in conditions:
            whereList.append(f"email ilike '%{conditions['email']}%'")
        
            
        whereConditions = "WHERE " + ' AND '.join(whereList)
        return whereConditions
