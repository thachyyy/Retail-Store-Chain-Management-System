import logging
import uuid
from typing import Optional

from datetime import date, timedelta
from sqlalchemy.orm import Session
from pydantic import UUID4

from app import crud
from app.services.invoice_for_customer import InvoiceForCustomerService
from app.services.batch import BatchService
from app.constant.app_status import AppStatus
# from app.schemas.dashboard import DashboardResponse, DashboardCreate, DashboardCreateParams, DashboardUpdate
from app.utils import hash_lib
from app.core.exceptions import error_exception_handler

from datetime import datetime

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
        
        
        # get avg price - giá trị đơn hàng trung bình
        avg = total_sales / total_order
        avg_price = round(avg, 2)
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
        
        
        # get avg product - kích thước giỏ hàng trung bình
        avg_prod = product_sold / total_order
        avg_product = round(avg_prod)
        # -------------------------------------------------------
        
        
        # get total new customer
        total_new_customer = await crud.dashboard.get_total_new_customer(self.db, start_date, end_date, tenant_id, branch)
        # -------------------------------------------------------
        
        
        # get cost
        list_batch = dict()
        for invoice in list_invoice:
            for order_detail in invoice.order_detail:
                if order_detail.batch_id in list_batch:
                    list_batch[order_detail.batch_id][1] += order_detail.quantity
                else:
                    import_price = await crud.dashboard.get_import_price(self.db, order_detail.batch_id, tenant_id, branch)
                    list_batch[order_detail.batch_id] = [import_price, order_detail.quantity]
                    
        cost = 0
        for batch in list_batch.items():
            cost += batch[1][0] * batch[1][1]
        # -------------------------------------------------------
        
        
        # get profit
        profit = total_sales - cost
        # -------------------------------------------------------
        
        
        response = dict()
        response['total_sales'] = total_sales
        response['cost'] = cost
        response['profit'] = profit
        response['total_order'] = total_order
        response['avg_price'] = avg_price
        response['avg_product'] = avg_product
        response['product_sold'] = product_sold
        response['new_customer'] = total_new_customer
        
        logger.info("DashboardService: sales_summary is called successfully.")
        return response
        
    async def sales_report_by_product(self, tenant_id: str, branch: str):
        logger.info("ServiceReport: sales_report_by_product is called.")
        invoice_service = InvoiceForCustomerService(db=self.db)
        msg, list_invoice = await invoice_service.get_all_invoice_for_customers(
            tenant_id=tenant_id, 
            branch=branch
        )
        list_product_quantity = dict()
        
        for invoice in list_invoice:
            for order_detail in invoice.order_detail:
                if order_detail.product_id in list_product_quantity:
                    list_product_quantity[order_detail.product_id][2] += order_detail.quantity
                else:
                    quantity = order_detail.quantity
                    name, price = await crud.report.get_price_and_name_by_product_id(self.db, order_detail.product_id, tenant_id, branch)
                    list_product_quantity[order_detail.product_id] = [name, price, quantity]
            # print("list product:", list_product_quantity)
        
        # tính doanh thu bằng số lượng nhân giá bán
        for product_id, details in list_product_quantity.items():
            name = details[0]
            price = details[1]
            quantity = details[2]
            
            revenue = price * quantity
            
            details.append(revenue)
        return list_product_quantity
    
    # async def get_sell_through_rate1(self, tenant_id: str, branch: str):
    #     invoice_for_customer_service = InvoiceForCustomerService(db=self.db)
    #     product_response= await crud.dashboard.get_all_product_id_name_price(self.db, tenant_id, branch)
        
    #     result = []
    #     flag = 0
    #     latest_batch = datetime.now()
    #     batch_service = BatchService(db=self.db)
        
    #     for prod in product_response:
    #         inventory = 0
    #         sales_total = 0
    #         sold = 0
            
    #         msg, batch_response = await batch_service.get_all_batches(tenant_id=tenant_id,
    #                                                              branch=branch,
    #                                                              query_search = prod['id'])
            
    #         latest_import = 0
    #         for batch in batch_response:
    #             if flag == 1:
    #                 latest_batch =  batch.created_at
    #                 latest_import = batch.quantity
                    
    #             if flag == 0:
    #                 # Ngày nhập mới nhất
    #                 newest_batch = batch.created_at
    #                 flag += 1

    #             print("flaggggg", flag)
    #             print("latest_batchhhhhhh", latest_batch)
    #             print("newest_batchhhhh", newest_batch)
    #             print("latest_importttttttt", latest_import)
        
    #     return "Success"