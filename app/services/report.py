import logging
from typing import Optional, Literal

from sqlalchemy.orm import Session
from pydantic import UUID4

from app import crud
from app.services.invoice_for_customer import InvoiceForCustomerService
from app.services.dashboard import DashboardService
from app.constant.app_status import AppStatus
from app.core.exceptions import error_exception_handler
from fastapi import FastAPI, Response, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
import pdfkit
from starlette.responses import FileResponse
from fastapi.responses import Response
from datetime import date, timedelta
from uuid import uuid4
from fastapi.responses import JSONResponse
from app.core.s3 import S3ServiceSingleton
import io

s3_service = S3ServiceSingleton()
SUPPORTED_FILE_TYPES = {
    'image/png': 'png',
    'image/jpeg': 'jpg',
    'application/pdf': 'pdf'
}

logger = logging.getLogger(__name__)

class ReportService:
    def __init__(self, db: Session):
        self.db = db
      
    async def report_inventory_quantity(self, user_id: str, tenant_id: str, branch: str = None):
        logger.info("ReportService: report_inventory_quantity is called.")
        if branch == "Tất cả chi nhánh":
            branch = None
        user_name = await crud.report.get_user_name(self.db, user_id)
        list_result = await crud.report.report_inventory_quantity(self.db, tenant_id, branch)
            
        time_report = date.today()
        # Bắt đầu tạo mã HTML
        html_output = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
        <meta charset="UTF-8">
        <title>Báo Cáo Lượng Hàng Tồn Kho</title>
        <style>
            table, th, td {
                border: 1px solid black;
                border-collapse: collapse;
            }
            th, td {
                padding: 8px;
                text-align: left;
            }
            th {
                background-color: #f2f2f2;
            }
        </style>
        </head>
        <body>"""
        
        if branch is None:
          branch = "Tất cả chi nhánh"
        
        html_output += f"""
        <h1>BÁO CÁO HÀNG LƯỢNG HÀNG TỒN KHO</h1>
        <h2>Tên công ty: {tenant_id}</h2>
        <h2>{branch}</h2>
        <p>Người tạo báo cáo: {user_name}</p>
        <p>Ngày xuất báo cáo: {time_report}</p>
        <table>
            <tr>
                <th>Mã sản phẩm</th>
                <th>Tên sản phẩm</th>
                <th>Số lượng tồn kho</th>
            </tr>
        """

        # Thêm dòng cho mỗi hàng dữ liệu
        for item in list_result:
            html_output += f"""
            <tr>
                <td>{item['product_id']}</td>
                <td>{item['product_name']}</td>
                <td>{item['total_quantity']}</td>
            </tr>
            """

        # Kết thúc HTML
        html_output += """
            </table>

            </body>
            </html>
            """
      
        # print("html output", html_output)
        
        pdf = pdfkit.from_string(html_output, False)
        
        res = io.BytesIO(pdf)
        public_url = self.upload_pdf(res)
        
        return public_url
        
    async def sales_report_by_branch(self, user_id: str, start_date: date, end_date: date, tenant_id: str):
        logger.info("ReportService: report_inventory_quantity is called.")
        user_name = await crud.report.get_user_name(self.db, user_id)
        
        end_date += timedelta(days=1)
        list_result = await crud.report.sales_report_by_branch(self.db, tenant_id, start_date, end_date)
        time_report = date.today()
        
        
        # Bắt đầu tạo mã HTML
        html_output = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
        <meta charset="UTF-8">
        <title>Báo Cáo Doanh Thu Theo Cửa Hàng</title>
        <style>
            table, th, td {
                border: 1px solid black;
                border-collapse: collapse;
            }
            th, td {
                padding: 8px;
                text-align: left;
            }
            th {
                background-color: #f2f2f2;
            }
        </style>
        </head>
        <body>"""
        
        end_date -= timedelta(days=1)
        html_output += f"""
        <h1>BÁO CÁO DOANH THU THEO CỬA HÀNG</h1>
        <h2>Tên công ty: {tenant_id}</h2>
        <p>Người tạo báo cáo: {user_name}</p>
        <p>Ngày xuất báo cáo: {time_report}</p>
        <p>Khoảng thời gian: {start_date} đến {end_date}</p>
        <table>
            <tr>
                <th>Cửa hàng</th>
                <th>Đơn bán hàng</th>
                <th>Doanh thu</th>
            </tr>
        """
        
        # Thêm dòng cho mỗi hàng dữ liệu
        for item in list_result:
            html_output += f"""
            <tr>
                <td>{item['branch']}</td>
                <td>{item['count']}</td>
                <td>{item['sum']}</td>
            </tr>
            """

        # Kết thúc HTML
        html_output += """
            </table>

            </body>
            </html>
            """
        
        pdf = pdfkit.from_string(html_output, False)
        
        res = io.BytesIO(pdf)
        public_url = self.upload_pdf(res)
        
        return public_url
    
    async def sales_report_by_product(self, user_id: str, start_date: date, end_date: date, tenant_id: str, branch: str = None):
        logger.info("ServiceReport: sales_report_by_product is called.")
        # invoice_service = InvoiceForCustomerService(db=self.db)
        user_name = await crud.report.get_user_name(self.db, user_id)
        end_date += timedelta(days=1)
        # msg, list_invoice = await invoice_service.get_all_invoice_for_customers(
        #     tenant_id=tenant_id, 
        #     branch=branch, 
        #     start_date=start_date, 
        #     end_date=end_date
        # )
        # list_product_quantity = dict()
        
        # for invoice in list_invoice:
        #     for order_detail in invoice.order_detail:
        #         if order_detail.product_id in list_product_quantity:
        #             list_product_quantity[order_detail.product_id][2] += order_detail.quantity
        #         else:
        #             quantity = order_detail.quantity
        #             name, price = await crud.report.get_price_and_name_by_product_id(self.db, order_detail.product_id, tenant_id, branch)
        #             list_product_quantity[order_detail.product_id] = [name, price, quantity]
        #     # print("list product:", list_product_quantity)
        
        # # tính doanh thu bằng số lượng nhân giá bán
        # for product_id, details in list_product_quantity.items():
        #     name = details[0]
        #     price = details[1]
        #     quantity = details[2]
            
        #     revenue = price * quantity
            
        #     details.append(revenue)
        # tính lợi nhuận lấy số lượng nhân (giá bán - giá nhập) // chưa làm
        
        
        dashboard_service = DashboardService(db=self.db)
        if branch == "Tất cả chi nhánh":
            branch = None
        products = await dashboard_service.get_all_sell_through_rate(tenant_id, branch)
        
        # tạo html
        time_report = date.today()
        # Bắt đầu tạo mã HTML
        html_output = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
        <meta charset="UTF-8">
        <title>Báo Cáo Doanh Thu Theo Sản Phẩm</title>
        <style>
            table, th, td {
                border: 1px solid black;
                border-collapse: collapse;
            }
            th, td {
                padding: 8px;
                text-align: left;
            }
            th {
                background-color: #f2f2f2;
            }
        </style>
        </head>
        <body>"""
        
        end_date -= timedelta(days=1)
        if branch is None:
            branch = "Tất cả chi nhánh"
        html_output += f"""
        <h1>BÁO CÁO DOANH THU THEO SẢN PHẨM</h1>
        <h2>Tên công ty: {tenant_id}</h2>
        <p>Chi nhánh: {branch}</p>
        <p>Người tạo báo cáo: {user_name}</p>
        <p>Ngày xuất báo cáo: {time_report}</p>
        <p>Khoảng thời gian: {start_date} đến {end_date}</p>
        <table>
            <tr>
                <th>Tên sản phẩm</th>
                <th>Giá bán</th>
                <th>Doanh thu</th>
                <th>Đã bán</th>
                <th>Tồn kho</th>
                <th>Tỷ lệ bán hết</th>
            </tr>
        """
        
        # Thêm dòng cho mỗi hàng dữ liệu
        for prod in products:
            html_output += f"""
            <tr>
                <td>{prod['product_name']}</td>
                <td>{prod['sale_price']}</td>
                <td>{prod['sales_total']}</td>
                <td>{prod['sold']}</td>
                <td>{prod['inventory']}</td>
                <td>{round(prod['sell_rate'], 2)}</td>
            </tr>
            """

        # Kết thúc HTML
        html_output += """
            </table>

            </body>
            </html>
            """
        
        pdf = pdfkit.from_string(html_output, False)
        
        res = io.BytesIO(pdf)
        public_url = self.upload_pdf(res)
        
        return public_url
    
    async def sales_report_by_customer(self, user_id: str, start_date: date, end_date: date, tenant_id: str, branch: str):
        logger.info("ServiceReport: sales_report_by_customer is called.")
        
        user_name = await crud.report.get_user_name(self.db, user_id)
        end_date += timedelta(days=1)
        if branch == "Tất cả chi nhánh":
            branch = None
        result_list = await crud.report.sales_report_by_customer(self.db, start_date, end_date, tenant_id, branch)
        
        
        time_report = date.today()
        # Bắt đầu tạo mã HTML
        html_output = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
        <meta charset="UTF-8">
        <title>Báo Cáo Doanh Thu Theo Khách Hàng</title>
        <style>
            table, th, td {
                border: 1px solid black;
                border-collapse: collapse;
            }
            th, td {
                padding: 8px;
                text-align: left;
            }
            th {
                background-color: #f2f2f2;
            }
        </style>
        </head>
        <body>"""
        
        end_date -= timedelta(days=1)
        if branch is None:
            branch = "Tất cả chi nhánh"
        html_output += f"""
        <h1>BÁO CÁO DOANH THU THEO KHÁCH HÀNG</h1>
        <h2>Tên công ty: {tenant_id}</h2>
        <p>Chi nhánh: {branch}</p>
        <p>Người tạo báo cáo: {user_name}</p>
        <p>Ngày xuất báo cáo: {time_report}</p>
        <p>Khoảng thời gian: {start_date} đến {end_date}</p>
        <table>
            <tr>
                <th>Mã khách hàng</th>
                <th>Tên khách hàng</th>
                <th>Doanh thu</th>
            </tr>
        """
        
        # Thêm dòng cho mỗi hàng dữ liệu
        for item in result_list:
            html_output += f"""
            <tr>
                <td>{item['customer_id']}</td>
                <td>{item['full_name']}</td>
                <td>{item['sum']}</td>
            </tr>
            """

        # Kết thúc HTML
        html_output += """
            </table>

            </body>
            </html>
            """
        
        pdf = pdfkit.from_string(html_output, False)
        
        res = io.BytesIO(pdf)
        public_url = self.upload_pdf(res)
        
        return public_url
    
    async def sales_report_by_categories(self, user_id: str, start_date: date, end_date: date, tenant_id: str, branch: str):
        logger.info("ServiceReport: sales_report_by_categories is called.")
        invoice_service = InvoiceForCustomerService(db=self.db)
        user_name = await crud.report.get_user_name(self.db, user_id)
        end_date += timedelta(days=1)
        if branch == "Tất cả chi nhánh":
            branch = None
        msg, list_invoice = await invoice_service.get_all_invoice_for_customers(
            tenant_id=tenant_id, 
            branch=branch, 
            start_date=start_date, 
            end_date=end_date
        )
        
        list_categories_quantity = dict()
        
        for invoice in list_invoice:
            for order_detail in invoice.order_detail:
                # categories_id = await crud.report.get_categories_of_product(self.db, order_detail.product_id, tenant_id, branch)
                categories_name = await crud.report.get_categories_name_of_product(self.db, order_detail.product_id, tenant_id, branch)
                if categories_name.lower() in list_categories_quantity:
                    price = await crud.report.get_price_of_product(self.db, order_detail.product_id, tenant_id, branch)
                    total = order_detail.quantity * price
                    list_categories_quantity[categories_name][0] += order_detail.quantity
                    list_categories_quantity[categories_name][1] += total                    
                else:
                    quantity = order_detail.quantity
                    price = await crud.report.get_price_of_product(self.db, order_detail.product_id, tenant_id, branch)
                    total = quantity * price
                    # name = await crud.report.get_name_by_categories_id(self.db, categories_id, tenant_id, branch)
                    list_categories_quantity[categories_name.lower()] = [quantity, total]
        
        # print(list_categories_quantity)
        # tạo html
        time_report = date.today()
        # Bắt đầu tạo mã HTML
        html_output = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
        <meta charset="UTF-8">
        <title>Báo Cáo Doanh Thu Theo Nhóm Sản Phẩm</title>
        <style>
            table, th, td {
                border: 1px solid black;
                border-collapse: collapse;
            }
            th, td {
                padding: 8px;
                text-align: left;
            }
            th {
                background-color: #f2f2f2;
            }
        </style>
        </head>
        <body>"""
        
        end_date -= timedelta(days=1)
        if branch is None:
            branch = "Tất cả chi nhánh"
        html_output += f"""
        <h1>BÁO CÁO DOANH THU THEO NHÓM SẢN PHẨM</h1>
        <h2>Tên công ty: {tenant_id}</h2>
        <p>Chi nhánh: {branch}</p>
        <p>Người tạo báo cáo: {user_name}</p>
        <p>Ngày xuất báo cáo: {time_report}</p>
        <p>Khoảng thời gian: {start_date} đến {end_date}</p>
        <table>
            <tr>
                <th>Tên nhóm sản phẩm</th>
                <th>Số lượng sản phẩm</th>
                <th>Doanh thu</th>
            </tr>
        """
        
        # Thêm dòng cho mỗi hàng dữ liệu
        for categories_name, details in list_categories_quantity.items():
            html_output += f"""
            <tr>
                <td>{categories_name}</td>
                <td>{details[0]}</td>
                <td>{details[1]}</td>
            </tr>
            """

        # Kết thúc HTML
        html_output += """
            </table>

            </body>
            </html>
            """
        
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
            file_path = f'report/{uuid4()}.{file_extension}'
            # Upload to S3 and get the public URL
            public_url = s3_service.upload_image_object(file_content, file_path, content_type)
            
            # if file_extension in ['png', 'jpg']:
            #     await crud.product.insert_img_url(db=db, tenant_id=current_user.tenant_id, url=public_url, product_id=product_id)
            # else:
            #     await crud.contract_for_vendor.insert_pdf_url(db=db, tenant_id=current_user.tenant_id, url=public_url, contract_id=contract_id)

            return JSONResponse(status_code=200, content={"message": "File uploaded successfully", "url": public_url})
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))