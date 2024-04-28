import logging
import uuid
from typing import Optional

from datetime import date, timedelta
from sqlalchemy.orm import Session
from pydantic import UUID4

from app import crud
from app.services.invoice_for_customer import InvoiceForCustomerService
from app.constant.app_status import AppStatus
# from app.schemas.dashboard import DashboardResponse, DashboardCreate, DashboardCreateParams, DashboardUpdate
from app.utils import hash_lib
from app.core.exceptions import error_exception_handler

logger = logging.getLogger(__name__)

class DashboardService:
    def __init__(self, db: Session):
        self.db = db
    
    async def get_total_sale_by_branch(self, tenant_id: str = None, branch: str = None):
        logger.info("DashboardService: get_total_sale_by_id called.")
        # result = await crud.dashboard.get_total_sale_by_id(db=self.db, tenant_id=tenant_id, branch=branch)
        
        
        return dict(message_code=AppStatus.SUCCESS.message)
    
    async def sales_summary(self, start_date: date, end_date: date, tenant_id: str, branch: str = None):
        logger.info("DashboardService: sales_summary is called.")
        
        end_date += timedelta(days=1)
        
        # get total sale
        total_sales = await crud.dashboard.get_total_sales(self.db, start_date, end_date, tenant_id, branch)
        # -------------------------------------------------------
        
        
        # get total order
        total_order = await crud.dashboard.get_total_order(self.db, start_date, end_date, tenant_id, branch)
        # -------------------------------------------------------
        
        
        # get product_sold
        invoice_service = InvoiceForCustomerService(db=self.db)
        msg, list_invoice = await invoice_service.get_all_invoice_for_customers(
            tenant_id=tenant_id, 
            branch=branch, 
            start_date=start_date, 
            end_date=end_date
        )
        list_product_quantity = dict()
        
        for invoice in list_invoice:
            for order_detail in invoice.order_detail:
                if order_detail.product_id in list_product_quantity:
                    list_product_quantity[order_detail.product_id] += order_detail.quantity
                else:
                    quantity = order_detail.quantity
                    list_product_quantity[order_detail.product_id] = quantity
        
        product_sold = 0
        for k, v in list_product_quantity.items():
            product_sold += v
        # -------------------------------------------------------
        
        
        # get total new customer
        total_new_customer = await crud.dashboard.get_total_new_customer(self.db, start_date, end_date, tenant_id, branch)
        # -------------------------------------------------------
        response = dict()
        response['total_sales'] = total_sales
        response['total_order'] = total_order
        response['product_sold'] = product_sold
        response['new_customer'] = total_new_customer
        
        logger.info("DashboardService: sales_summary is called successfully.")
        return response
        