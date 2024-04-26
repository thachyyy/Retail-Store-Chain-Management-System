import logging
from typing import Optional, Literal

from sqlalchemy.orm import Session
from pydantic import UUID4

from app import crud
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
        # for row in list_result:
            # print("product_id", row['product_id'])
            # print("product_name", row['product_name'])
            # print("total_quantity", row['total_quantity'])
            # print("----------------------------------")
            
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
          branch = "Toàn bộ các chi nhánh"
        
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
            
        # print("html output", html_output)
        
        pdf = pdfkit.from_string(html_output, False)
        
        headers = {
            'Content-Disposition': f"attachment;filename=sales-report-by-branch.pdf"
        }
        
        logger.info("ReportService: report_inventory_quantity is called successfully.")
        return Response(content=pdf, headers=headers, media_type='application/pdf')
    
    # async def sales_report_by_product(self, user_id: str, start_date: date, end_date: date, tenant_id: str, branch: str):
    #     pass