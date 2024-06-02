
import json
import logging
import uuid
from typing import Optional

from datetime import date, timedelta
from fastapi import File, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from pydantic import UUID4
from app.core.s3 import S3ServiceSingleton
import pdfkit
import io
from app import crud
from app.constant.app_status import AppStatus
from app.schemas.invoice_for_customer import InvoiceForCustomerResponse, InvoiceForCustomerCreate, InvoiceForCustomerCreateParams, InvoiceForCustomerUpdate
from app.utils import hash_lib
from app.core.exceptions import error_exception_handler
from datetime import datetime
logger = logging.getLogger(__name__)
s3_service = S3ServiceSingleton()
SUPPORTED_FILE_TYPES = {
    'image/png': 'png',
    'image/jpeg': 'jpg',
    'application/pdf': 'pdf'
}
class InvoiceForCustomerService:
    def __init__(self, db: Session):
        self.db = db
    
    async def get_invoice_for_customer_by_id(self, invoice_for_customer_id: str, tenant_id: str):
        logger.info("InvoiceForCustomerService: get_invoice_for_customer_by_id called.")
        result = await crud.invoice_for_customer.get_invoice_for_customer_by_id(db=self.db, invoice_for_customer_id=invoice_for_customer_id, tenant_id=tenant_id)
        logger.info("InvoiceForCustomerService: get_invoice_for_customer_by_id called successfully.")
        response = []
        
        r = await self.make_response_invoice(result)
        response.append(r)
        return dict(message_code=AppStatus.SUCCESS.message), response[0]
    
    async def get_all_invoice_for_customers(
        self,
        tenant_id: str,
        branch: Optional[str] = None,
        limit: Optional[int] = None,
        offset:Optional[int] = None,
        status:Optional[str] = None,
        gt_total:Optional[int] = None,
        lt_total:Optional[int] = None,
        start_date:Optional[date] = None,
        end_date:Optional[date] = None,
        start_date_1:Optional[datetime] = None,
        end_date_1:Optional[datetime] = None,
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
            end_date += timedelta(days=1)
            conditions['end_date'] = end_date
        if start_date_1:
            conditions['start_date_1'] = start_date_1
        if end_date_1:  
            conditions['end_date_1'] = end_date_1    
        
        
        if conditions:
            whereConditions = await self.whereConditionBuilderForFilter(tenant_id, conditions, branch)
            sql = f"SELECT * FROM public.invoice_for_customer {whereConditions};"
            
            if limit is not None and offset is not None:
                sql = f"SELECT * FROM public.invoice_for_customer {whereConditions} LIMIT {limit} OFFSET {offset*limit};"
            
            total = f"SELECT COUNT(*) FROM public.invoice_for_customer {whereConditions};"

            logger.info("InvoiceForCustomerService: filter_invoice_for_customer called.")
            result,total= await crud.invoice_for_customer.get_invoice_for_customer_by_conditions(self.db, sql=sql,total = total)
            total = total[0]['count']
        elif query_search:
            whereConditions = await self.whereConditionBuilderForSearch(tenant_id, query_search, branch)
            
            sql = f"SELECT * FROM public.invoice_for_customer {whereConditions};"
            
            if limit is not None and offset is not None:
                sql = f"SELECT * FROM public.invoice_for_customer {whereConditions} LIMIT {limit} OFFSET {offset*limit};"
                
            
            total = f"SELECT COUNT(*) FROM public.invoice_for_customer {whereConditions};"

            logger.info("InvoiceForCustomerService: filter_invoice_for_customer called.")
            result,total= await crud.invoice_for_customer.get_invoice_for_customer_by_conditions(self.db, sql=sql,total = total)
            total = total[0]['count']
        else: 
            logger.info("InvoiceForCustomerService: get_all_invoice_for_customer called.")
            sql = f"SELECT COUNT(*) FROM public.invoice_for_customer WHERE tenant_id = '{tenant_id}' AND branch = '{branch}';"
            if limit is not None and offset is not None:
                result, total = await crud.invoice_for_customer.get_all_invoice_for_customers(db=self.db,sql=sql,offset=offset*limit,limit=limit,tenant_id=tenant_id,branch=branch)
                total = total[0]['count']
            else: 
                result, total = await crud.invoice_for_customer.get_all_invoice_for_customers(db=self.db,sql=sql,tenant_id=tenant_id,branch=branch)             
                total = total[0]['count']
                logger.info("InvoiceForCustomerService: get_all_invoice_for_customer called successfully.")
                
                
        response = []
        for x in result:
            r = await self.make_response_invoice(x)
            response.append(r)
        
        return dict(message_code=AppStatus.SUCCESS.message, total=total), response
    
    async def make_response_invoice(self, obj_in):
        
        customer_name = await crud.invoice_for_customer.get_customer_name(self.db, obj_in.belong_to_order)
        
        response = InvoiceForCustomerResponse(
            id=obj_in.id,
            created_at=obj_in.created_at,
            updated_at=obj_in.updated_at,
            total=obj_in.total,
            payment_method=obj_in.payment_method,
            status=obj_in.status,
            belong_to_order= obj_in.belong_to_order,
            tenant_id = obj_in.tenant_id,
            branch= obj_in.branch,
            belong_to_customer=customer_name,
            order_detail=[]
        )
        # lenght_order_details = len(obj_in.order_detail)
        # idx = 0
        for id in obj_in.order_detail:
            order_detail = await crud.invoice_for_customer.get_order_detail_by_id(self.db, id)

            response.order_detail.append(order_detail)

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
                                          obj_in: InvoiceForCustomerCreateParams,
                                          tenant_id:str,
                                          branch: str
    ):
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
            belong_to_order=obj_in.belong_to_order,
            order_detail=obj_in.order_detail,
            tenant_id=tenant_id,
            branch=branch
        )   
        
        logger.info("InvoiceForCustomerService: create called.")
        result = crud.invoice_for_customer.create(db=self.db, obj_in=invoice_for_customer_create)
        logger.info("InvoiceForCustomerService: create called successfully.")
        
        self.db.commit()
        logger.info("Service: create_invoice_for_customer success.")
        return dict(message_code=AppStatus.SUCCESS.message), invoice_for_customer_create
    
    async def update_invoice_for_customer(self, invoice_for_customer_id: str, obj_in: InvoiceForCustomerUpdate, tenant_id: str):
        logger.info("InvoiceForCustomerService: get_invoice_for_customer_by_id called.")
        isValidInvoiceForCustomer = await crud.invoice_for_customer.get_invoice_for_customer_by_id(db=self.db, invoice_for_customer_id=invoice_for_customer_id,tenant_id=tenant_id)
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
        obj_update = await crud.invoice_for_customer.get_invoice_for_customer_by_id(self.db, invoice_for_customer_id,tenant_id)
        return dict(message_code=AppStatus.UPDATE_SUCCESSFULLY.message), obj_update
        
    async def delete_invoice_for_customer(self, invoice_for_customer_id: str, tenant_id: str):
        logger.info("InvoiceForCustomerService: get_invoice_for_customer_by_id called.")
        isValidInvoiceForCustomer = await crud.invoice_for_customer.get_invoice_for_customer_by_id(db=self.db, invoice_for_customer_id=invoice_for_customer_id, tenant_id=tenant_id)
        logger.info("InvoiceForCustomerService: get_invoice_for_customer_by_id called successfully.")
        
        if not isValidInvoiceForCustomer:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_CUSTOMER_NOT_FOUND)
        
        obj_del = await crud.invoice_for_customer.get_invoice_for_customer_by_id(self.db, invoice_for_customer_id)
        
        logger.info("InvoiceForCustomerService: delete_invoice_for_customer called.")
        result = await crud.invoice_for_customer.delete_invoice_for_customer(self.db, invoice_for_customer_id)
        logger.info("InvoiceForCustomerService: delete_invoice_for_customer called successfully.")
        
        self.db.commit()
        return dict(message_code=AppStatus.DELETED_SUCCESSFULLY.message), obj_del
    
    async def whereConditionBuilderForSearch(self, tenant_id: str, condition: str, branch: str = None) -> str:
        conditions = list()
        conditions.append(f"id::text ilike '%{condition}%'")
            
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
        
        if 'status' in conditions:
            whereList.append(f"LOWER(status) = LOWER('{conditions['status']}')")
        if 'gt_total' in conditions:
            whereList.append(f"total >= '{conditions['gt_total']}'")
        if 'lt_total' in conditions:
            whereList.append(f"total <= '{conditions['lt_total']}'")
        if 'start_date' in conditions:
            whereList.append(f"created_at >= '{conditions['start_date']}'")
        if 'end_date' in conditions:
            whereList.append(f"created_at <= '{conditions['end_date']}'")
        if 'start_date_1' in conditions:
            whereList.append(f"created_at >= '{conditions['start_date_1']}'")
        if 'end_date_1' in conditions:
            whereList.append(f"created_at <= '{conditions['end_date_1']}'")    
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
    
    
    async def invoice_print(self,invoice_id:str ,user_id: str, tenant_id: str, branch: str = None):
        
        # TODO: phân tích hiện thực ở đây
        logger.info("ServiceReport: sales_report_by_categories is called.")
        invoice_service = InvoiceForCustomerService(db=self.db)
        user_name = await crud.report.get_user_name(self.db, user_id)
        if branch == "Tất cả chi nhánh":
            branch = None
            
        msg, invoice_for_cus = await invoice_service.get_invoice_for_customer_by_id(
            invoice_for_customer_id=invoice_id,
            tenant_id=tenant_id
        )
        print("invoice_for_cus:",invoice_for_cus)
        if invoice_for_cus.belong_to_customer != None:
            customer_name = invoice_for_cus.belong_to_customer
        else:
            customer_name = ""
        # Tạo form phân tích
        
        
        time_report = date.today()
        # Bắt đầu tạo mã HTML
        html_output = """
         <!DOCTYPE html>
            <html lang="en">
            <head>
            <meta charset="UTF-8">
            <title>Sales Invoice</title>
            <style>
                body { font-family: Arial, sans-serif; }
                table { width: 100%; border-collapse: collapse; }
                th, td { border: 1px solid black; padding: 8px; text-align: left; }
                th { background-color: #f2f2f2; }
                h1 { text-align: center; }
                .info { margin-bottom: 20px; }
                .total { text-align: right; font-weight: bold; }
            </style>
            </head>
            <body> 
        """
        
        if branch is None:
           branch = "Tất cả chi nhánh"
        
        html_output += f"""
            <h1>HÓA ĐƠN BÁN HÀNG</h1>
            <div class="info">
                <p><strong>ID hóa đơn:</strong> {invoice_id} </p>
                <p><strong>Chi nhánh:</strong> {branch}</p>
                <p><strong>Tên nhân viên:</strong> {user_name}</p>
                <p><strong>Tên khách hàng:</strong> {customer_name}</p>
                <p><strong>Ngày tạo hóa đơn:</strong> {invoice_for_cus.created_at.date()}</p>
                <p><strong>Ngày in hóa đơn:</strong> {time_report}</p>
            </div>
        
        <table>
             <tr>
                <th>STT</th>
                <th>Sản phẩm</th>
                <th>Số lượng</th>
                <th>Đơn giá</th>
                <th>Thành tiền</th>
            </tr>

        """

        # Thêm dòng cho mỗi hàng dữ liệu, lặp trong list trả về (tên list thay đổi cho đúng)
        i = 1
        for item in invoice_for_cus.order_detail:
            html_output += f"""
            <tr>
                <td> {i} </td>
                <td>{item.product_name}</td>
                <td>{item.quantity}</td>
                <td>{item.price}</td>
                <td>{item.sub_total}</td>
            </tr>
            """
            i+= 1
        # Kết thúc HTML
        html_output += f"""
            </table>
            <p class="total">Tổng tiền: {invoice_for_cus.total}</p>
            </body>
            </html>
            """
      
        # print("html output", html_output)
        
        pdf = pdfkit.from_string(html_output, False)
        
        res = io.BytesIO(pdf)
        public_url = self.upload_pdf(res)
        
        return public_url
    
    def upload_pdf(self, file: UploadFile = File(...)):
        try:
            # Read image file
            file_content = file.read()
            
            # Define the file path where the image will be stored on S3
            # file_path = file.filename  

            content_type = "application/pdf" 
            file_extension = SUPPORTED_FILE_TYPES[content_type]
            file_path = f'report/{uuid.uuid4()}.{file_extension}'
            # Upload to S3 and get the public URL
            public_url = s3_service.upload_image_object(file_content, file_path, content_type)
            
            # if file_extension in ['png', 'jpg']:
            #     await crud.product.insert_img_url(db=db, tenant_id=current_user.tenant_id, url=public_url, product_id=product_id)
            # else:
            #     await crud.contract_for_vendor.insert_pdf_url(db=db, tenant_id=current_user.tenant_id, url=public_url, contract_id=contract_id)

            return JSONResponse(status_code=200, content={"message": "File uploaded successfully", "url": public_url})
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))