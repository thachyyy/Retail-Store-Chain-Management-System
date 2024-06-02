import logging
from typing import Optional
import uuid
from fastapi import HTTPException
from sqlalchemy.orm import Session
from pydantic import UUID4
from datetime import date, datetime, timedelta

from app import crud
from app.api.endpoints.dashboard import get_all_sell_through_rate_for_info
from app.constant.app_status import AppStatus
from app.models.import_detail import ImportDetail
from app.schemas.import_detail import ImportDetailCreate, ImportDetailCreateParams
from app.schemas.info import  InfoCreate, InfoUpdate, InvoiceOrderResponse
from app.core.exceptions import error_exception_handler
from app.schemas.product import ProductCreate, ProductCreateParams
from app.services.batch import BatchService
from app.services.import_order import ImportOrderService
from app.services.invoice_for_customer import InvoiceForCustomerService
from app.services.product_1 import ProductService

logger = logging.getLogger(__name__)

class InfoService:
    def __init__(self, db: Session):
        self.db = db
    async def get_info_by_product_id(
        self, 
        product_id:str,
        tenant_id:str,
        branch:str
        ):
        list_info = await crud.info.get_info_id(product_id=product_id,tenant_id=tenant_id,branch=branch,db=self.db)
        logger.info("Service: create_info success.")
        return dict(message_code=AppStatus.SUCCESS.message), list_info
        
    async def get_info(
        self, 
        tenant_id:str,
        branch:str
        ):
        list_info = await crud.info.get_all_info(tenant_id=tenant_id,branch=branch,db=self.db)
        logger.info("Service: create_info success.")
        return dict(message_code=AppStatus.SUCCESS.message), list_info
    
    async def add_new_info(
        self, 
        product: ProductCreate,
        tenant_id:str,
        branch:str):
        category ="A"
        sold = 0
        sell_rate = 0.0
        inventory = 0.0
        info_obj = InfoCreate(
                product_id=product.id,
                product_name=product.product_name,
                sale_price=product.sale_price,
                sold=sold,
                sale_rate=round(sell_rate,2),
                inventory=inventory,
                category=category,
                branch=branch,
                tenant_id=tenant_id
            )
        logger.info("InfoService: create called.")
        
        result = await crud.info.create(db=self.db, obj_in=info_obj)
        logger.info("InfoService: create called successfully.")

        self.db.commit()
        list_info = await crud.info.get_all_info(tenant_id=tenant_id,branch=branch,db=self.db)
        logger.info("Service: create_info success.")
        return dict(message_code=AppStatus.SUCCESS.message), list_info
    
    async def create_info(
        self, 
        tenant_id:str,
        branch:str
        ):
        # product_service = ProductService(self.db)
        # list_product = await product_service.get_list_product(tenant_id=tenant_id,branch=branch)
        # obj_in = get_all_sell_through_rate_for_info(branch=branch) 
        
    
        product_service = ProductService(self.db)
        logger.info("Endpoints: get_all_products called.")
        product_response= await product_service.get_all_products(tenant_id, branch)
        logger.info("Endpoints: get_all_products called successfully.")
        #product_name
        #sale_price 
        #ton kho  -> tong so luong cac lo
        #da ban -> invoice.quantity
        #doanh thu -> invoice.total
        #ti le ban het -> (sold / received (newest received)) * 100

        # 
        list_product = []
        for product in product_response[1]:
            if product.id not in list_product:
                list_product += [product.id]
        invoice_for_customer_service = InvoiceForCustomerService(self.db)   
        flag = 0
        latest_batch = datetime.now()
        for id in list_product:
            inventory = 0
            sales_total = 0
            sold = 0
            product = await crud.product.get_product_by_id(self.db,tenant_id=tenant_id,branch=branch,product_id=id)
            batch_service = BatchService(self.db)
            
            # Danh sách Lô theo thứ tự Lô mới nhất -> cũ nhất
            batch_response = await batch_service.get_all_batches(tenant_id=tenant_id,
                branch=branch,
                query_search = id)
            
        
            
            latest_import = 0
        
            ###############################
            import_order_service = ImportOrderService(self.db)
            import_order_response = await import_order_service.get_all_import_orders(tenant_id=tenant_id,branch=branch)
            
            
            for import_order in import_order_response[1]:
            
                if flag == 1:
                    latest_batch =  import_order.created_at
                    # latest_import = batch.quantity
                    for item in import_order.list_import:
                        if item.product_id == id:
                            latest_import = item.quantity   
                if flag == 0:
                    # Ngày nhập mới nhất
                    newest_batch = import_order.created_at
                    flag += 1
            
                
            ###############################
            for batch in batch_response[1]:
                inventory += batch.quantity

            list_invoice = await invoice_for_customer_service.get_all_invoice_for_customers(tenant_id=tenant_id, branch=branch)
        
            for invoice in list_invoice[1]:
                for order_detail in invoice.order_detail:
                    if order_detail.product_id == id:
                        sales_total += order_detail.price * order_detail.quantity
                        sold += order_detail.quantity

            sold_in_range = 0    
            if latest_batch:
                invoice_in_range =  await invoice_for_customer_service.get_all_invoice_for_customers(tenant_id=tenant_id, branch=branch,start_date=latest_batch,end_date=newest_batch)
                for invoice in invoice_in_range[1]:
                    for order_detail in invoice.order_detail:
                        if order_detail.product_id == id:
                            sold_in_range += order_detail.quantity
            
            if sold_in_range >= latest_import:    
                sell_rate = 100
            else:    
                if latest_import > 0:
                    # print("sold_in_range",sold_in_range)
                    # print("latest_import",latest_import)
                    sell_rate = (sold_in_range / latest_import )*100
                else: 
                    sell_rate = 0
            if sold_in_range == 0:
                sell_rate = 0
            category ="A"
            info_obj = InfoCreate(
                product_id=product.id,
                product_name=product.product_name,
                sale_price=product.sale_price,
                sold=sold,
                sale_rate=round(sell_rate,2),
                inventory=inventory,
                category=category,
                branch=branch,
                tenant_id=tenant_id
            )
            logger.info("InfoService: create called.")
            
            result = await crud.info.create(db=self.db, obj_in=info_obj)
            logger.info("InfoService: create called successfully.")

        self.db.commit()
        list_info = await crud.info.get_all_info(tenant_id=tenant_id,branch=branch,db=self.db)
        logger.info("Service: create_info success.")
        return dict(message_code=AppStatus.SUCCESS.message), list_info
    
    async def update_info(self, product_id: str, obj_in: InfoUpdate, tenant_id: str = None, branch: str = None):
        # logger.info("InfoService: get_info_by_id called.")
        # isValidInfo = await crud.info.get_info_by_id(db=self.db, id=info_id, branch=branch)
        # logger.info("InfoService: get_info_by_id called successfully.")
        
        logger.info("InfoService: update_info called.")
        
        result = await crud.info.update_info(db=self.db, product_id=product_id, info_update=obj_in,tenant_id=tenant_id,branch=branch)
        
        logger.info("InfoService: update_info called successfully.")
        self.db.commit()
        obj_update = await crud.info.get_info_product_id(product_id,tenant_id=tenant_id, branch=branch,db=self.db)
        return dict(message_code=AppStatus.UPDATE_SUCCESSFULLY.message), obj_update
    