
import logging
import uuid
from typing import Optional

from datetime import date
from sqlalchemy.orm import Session
from pydantic import UUID4

from app import crud
from app.constant.app_status import AppStatus
from app.schemas.invoice_for_customer import InvoiceForCustomerResponse, InvoiceForCustomerCreate, InvoiceForCustomerCreateParams, InvoiceForCustomerUpdate
from app.utils import hash_lib
from app.core.exceptions import error_exception_handler
from datetime import datetime
logger = logging.getLogger(__name__)

class InvoiceForCustomerService:
    def __init__(self, db: Session):
        self.db = db
    
    async def get_invoice_for_customer_by_id(self, invoice_for_customer_id: str):
        logger.info("InvoiceForCustomerService: get_invoice_for_customer_by_id called.")
        result = await crud.invoice_for_customer.get_invoice_for_customer_by_id(db=self.db, invoice_for_customer_id=invoice_for_customer_id)
        logger.info("InvoiceForCustomerService: get_invoice_for_customer_by_id called successfully.")
        
        return dict(message_code=AppStatus.SUCCESS.message), result
    
    async def get_all_invoice_for_customers(
        self,
        limit: Optional[int] = None,
        offset:Optional[int] = None,
        status:Optional[str] = None,
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
        
        
        if conditions:
            whereConditions = await self.whereConditionBuilderForFilter(conditions)
            sql = f"SELECT * FROM public.invoice_for_customer {whereConditions};"
            
            if limit is not None and offset is not None:
                sql = f"SELECT * FROM public.invoice_for_customer {whereConditions} LIMIT {limit} OFFSET {offset*limit};"
            
            total = f"SELECT COUNT(*) FROM public.invoice_for_customer {whereConditions};"

            logger.info("InvoiceForCustomerService: filter_invoice_for_customer called.")
            result,total= await crud.invoice_for_customer.get_invoice_for_customer_by_conditions(self.db, sql=sql,total = total)
            total = total[0]['count']
        
        elif query_search:
            whereConditions = await self.whereConditionBuilderForSearch(query_search)
            
            sql = f"SELECT * FROM public.invoice_for_customer {whereConditions};"
            
            if limit is not None and offset is not None:
                sql = f"SELECT * FROM public.invoice_for_customer {whereConditions} LIMIT {limit} OFFSET {offset*limit};"
                
            
            total = f"SELECT COUNT(*) FROM public.invoice_for_customer {whereConditions};"

            logger.info("InvoiceForCustomerService: filter_invoice_for_customer called.")
            result,total= await crud.invoice_for_customer.get_invoice_for_customer_by_conditions(self.db, sql=sql,total = total)
            total = total[0]['count']
        else: 
            logger.info("InvoiceForCustomerService: get_all_invoice_for_customer called.")
            sql = f"SELECT COUNT(*) FROM public.invoice_for_customer;"
            if limit is not None and offset is not None:
                result, total = await crud.invoice_for_customer.get_all_invoice_for_customers(db=self.db,sql=sql,offset=offset*limit,limit=limit)
                total = total[0]['count']
            else: 
                result, total = await crud.invoice_for_customer.get_all_invoice_for_customers(db=self.db,sql=sql)             
                total = total[0]['count']
                logger.info("InvoiceForCustomerService: get_all_invoice_for_customer called successfully.")
                
                
            response = []
            for x in result:
                r = await self.make_response_invoice(x)
                response.append(r)
        
        return dict(message_code=AppStatus.SUCCESS.message, total=total), response
    
    async def make_response_invoice(self, obj_in):
        response = InvoiceForCustomerResponse(
            id=obj_in.id,
            created_at=obj_in.created_at,
            updated_at=obj_in.updated_at,
            total=obj_in.total,
            payment_method=obj_in.payment_method,
            status=obj_in.status,
            order_details=[]
        )
        # lenght_order_details = len(obj_in.order_detail)
        # idx = 0
        for id in obj_in.order_detail:
            order_detail = await crud.invoice_for_customer.get_order_detail_by_id(self.db, id)

            response.order_details.append(order_detail)

            # if idx < lenght_order_details: idx += 1
            # else: break
            
        return response
    
    async def gen_id(self):
        newID: str
        lastID = await crud.invoice_for_customer.get_last_id(self.db)
        lenID = len(str(lastID))
        if lenID >= 9:
            return str(lastID + 1)
        else:
            newID = str(lastID + 1)
            len_rest = 9 - lenID
    
            for i in range(len_rest):
                newID = '0' + newID
    
            return 'INVOICECUS' + newID
        
    async def create_invoice_for_customer(self, 
                                          paid:bool,
                                          obj_in: InvoiceForCustomerCreateParams):
        newID = await self.gen_id()
        if paid == True:
            status = "Đã thanh toán"
        else:
            status = "Chưa thanh toán"      
        invoice_for_customer_create = InvoiceForCustomerCreate(
            id=newID,
            total=obj_in.total,
            status=status,
            payment_method=obj_in.payment_method,
            # belong_to_order=obj_in.belong_to_order,
            order_detail=obj_in.order_detail
        )
        
        logger.info("InvoiceForCustomerService: create called.")
        result = crud.invoice_for_customer.create(db=self.db, obj_in=invoice_for_customer_create)
        logger.info("InvoiceForCustomerService: create called successfully.")
        
        self.db.commit()
        logger.info("Service: create_invoice_for_customer success.")
        return dict(message_code=AppStatus.SUCCESS.message), invoice_for_customer_create
    
    async def update_invoice_for_customer(self, invoice_for_customer_id: str, obj_in: InvoiceForCustomerUpdate):
        logger.info("InvoiceForCustomerService: get_invoice_for_customer_by_id called.")
        isValidInvoiceForCustomer = await crud.invoice_for_customer.get_invoice_for_customer_by_id(db=self.db, invoice_for_customer_id=invoice_for_customer_id)
        logger.info("InvoiceForCustomerService: get_invoice_for_customer_by_id called successfully.")
        
        if not isValidInvoiceForCustomer:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_CUSTOMER_NOT_FOUND)
        
        if obj_in.belong_to_order:
            isValidOrder = await crud.purchase_order.get_purchase_order_by_id(self.db, obj_in.belong_to_order)
            if not isValidOrder:
                raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_PURCHASE_NOT_FOUND)
        
        logger.info("InvoiceForCustomerService: update_invoice_for_customer called.")
        result = await crud.invoice_for_customer.update_invoice_for_customer(db=self.db, invoice_for_customer_id=invoice_for_customer_id, invoice_for_customer_update=obj_in)
        logger.info("InvoiceForCustomerService: update_invoice_for_customer called successfully.")
        self.db.commit()
        obj_update = await crud.invoice_for_customer.get_invoice_for_customer_by_id(self.db, invoice_for_customer_id)
        return dict(message_code=AppStatus.UPDATE_SUCCESSFULLY.message), obj_update
        
    async def delete_invoice_for_customer(self, invoice_for_customer_id: str):
        logger.info("InvoiceForCustomerService: get_invoice_for_customer_by_id called.")
        isValidInvoiceForCustomer = await crud.invoice_for_customer.get_invoice_for_customer_by_id(db=self.db, invoice_for_customer_id=invoice_for_customer_id)
        logger.info("InvoiceForCustomerService: get_invoice_for_customer_by_id called successfully.")
        
        if not isValidInvoiceForCustomer:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_CUSTOMER_NOT_FOUND)
        
        obj_del = await crud.invoice_for_customer.get_invoice_for_customer_by_id(self.db, invoice_for_customer_id)
        
        logger.info("InvoiceForCustomerService: delete_invoice_for_customer called.")
        result = await crud.invoice_for_customer.delete_invoice_for_customer(self.db, invoice_for_customer_id)
        logger.info("InvoiceForCustomerService: delete_invoice_for_customer called successfully.")
        
        self.db.commit()
        return dict(message_code=AppStatus.DELETED_SUCCESSFULLY.message), obj_del
    
    async def whereConditionBuilderForSearch(self, condition: str) -> str:
        conditions = list()
        conditions.append(f"id::text ilike '%{condition}%'")
            
        whereCondition = "WHERE " + ' OR '.join(conditions)
        return whereCondition
    
    async def whereConditionBuilderForFilter(self, conditions: dict) -> str:
        whereList = list()
        
        if 'status' in conditions:
            whereList.append(f"status = '{conditions['status']}'")
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
    
    async def search_invoice_for_customer(self, condition: str = None):
        whereCondition = await self.whereConditionBuilderForSearch(condition)
        sql = f"SELECT * FROM public.invoice_for_customer {whereCondition};"
        
        logger.info("InvoiceForCustomerService: search_invoice_for_customer called.")
        result = await crud.invoice_for_customer.search_invoice_for_customer(self.db, sql)
        logger.info("InvoiceForCustomerService: search_invoice_for_customer called successfully.")
        
        return dict(message_code=AppStatus.SUCCESS.message), dict(data=result)
    
    async def filter_invoice_for_customer(
        self,
        gender: str = None,
        start_date: date = None,
        end_date: date = None,
        province: str = None,
        district: str = None,
):
        conditions = dict()
        if gender:
            conditions['gender'] = gender
        if start_date:
            conditions['start_date'] = start_date
        if end_date:
            conditions['end_date'] = end_date
        if province:
            conditions['province'] = province
        if district:
            conditions['district'] = district
        
        whereConditions = await self.whereConditionBuilderForFilter(conditions)
        sql = f"SELECT * FROM public.invoice_for_customer {whereConditions};"
        
        logger.info("InvoiceForCustomerService: filter_invoice_for_customer called.")
        result = await crud.invoice_for_customer.filter_invoice_for_customer(self.db, sql)
        logger.info("InvoiceForCustomerService: filter_invoice_for_customer called successfully.")
        
        return dict(message_code=AppStatus.SUCCESS.message), dict(data=result)
        