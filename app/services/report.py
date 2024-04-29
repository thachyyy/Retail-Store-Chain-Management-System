import logging
from typing import Optional, Literal

from sqlalchemy.orm import Session
from pydantic import UUID4

from app import crud
from app.services.invoice_for_customer import InvoiceForCustomerService
from app.constant.app_status import AppStatus
from app.core.exceptions import error_exception_handler
from fastapi import FastAPI, Response
from fastapi.responses import StreamingResponse
import pdfkit
from starlette.responses import FileResponse
from fastapi.responses import Response
from datetime import date, timedelta

logger = logging.getLogger(__name__)

class ReportService:
    def __init__(self, db: Session):
        self.db = db
      
    async def report_inventory_quantity(self, user_id: str, tenant_id: str, branch: str = None):
        logger.info("ReportService: report_inventory_quantity is called.")
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
        
        headers = {
            'Content-Disposition': f"attachment;filename=report-inventory-quantity.pdf"
        }
        
        logger.info("ReportService: report_inventory_quantity is called successfully.")
        return Response(content=pdf, headers=headers, media_type='application/pdf')
        

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
        
        headers = {
            'Content-Disposition': f"attachment;filename=sales-report-by-branch.pdf"
        }
        
        logger.info("ReportService: report_inventory_quantity is called successfully.")
        return Response(content=pdf, headers=headers, media_type='application/pdf')
    
    async def sales_report_by_product(self, user_id: str, start_date: date, end_date: date, tenant_id: str, branch: str = None):
        logger.info("ServiceReport: sales_report_by_product is called.")
        invoice_service = InvoiceForCustomerService(db=self.db)
        user_name = await crud.report.get_user_name(self.db, user_id)
        end_date += timedelta(days=1)
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
        # tính lợi nhuận lấy số lượng nhân (giá bán - giá nhập) // chưa làm
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
        <h1>BÁO CÁO DOANH THU THEO CỬA HÀNG</h1>
        <p>Chi nhánh: {branch}</p>
        <p>Người tạo báo cáo: {user_name}</p>
        <p>Ngày xuất báo cáo: {time_report}</p>
        <p>Khoảng thời gian: {start_date} đến {end_date}</p>
        <table>
            <tr>
                <th>Mã sản phẩm</th>
                <th>Tên sản phẩm</th>
                <th>Giá bán</th>
                <th>Số lượng</th>
                <th>Doanh thu</th>
            </tr>
        """
        
        # Thêm dòng cho mỗi hàng dữ liệu
        for product_id, details in list_product_quantity.items():
            html_output += f"""
            <tr>
                <td>{product_id}</td>
                <td>{details[0]}</td>
                <td>{details[1]}</td>
                <td>{details[2]}</td>
                <td>{details[3]}</td>
            </tr>
            """

        # Kết thúc HTML
        html_output += """
            </table>

            </body>
            </html>
            """
        
        pdf = pdfkit.from_string(html_output, False)
        
        headers = {
            'Content-Disposition': f"attachment;filename=sales-report-by-product.pdf"
        }
        
        logger.info("ReportService: sales_report_by_product is called successfully.")
        return Response(content=pdf, headers=headers, media_type='application/pdf')
    
    async def sales_report_by_customer(self, user_id: str, start_date: date, end_date: date, tenant_id: str, branch: str):
        logger.info("ServiceReport: sales_report_by_customer is called.")
        
        user_name = await crud.report.get_user_name(self.db, user_id)
        end_date += timedelta(days=1)
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
        
        headers = {
            'Content-Disposition': f"attachment;filename=sales-report-by-customer.pdf"
        }
        
        logger.info("ServiceReport: sales_report_by_customer is called successfully.")

        return Response(content=pdf, headers=headers, media_type='application/pdf')