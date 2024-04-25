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
from datetime import date

logger = logging.getLogger(__name__)

class ReportService:
    def __init__(self, db: Session):
        self.db = db
      
    async def report_inventory_quantity(self, user_id: str, tenant_id: str, branch: str = None):
        logger.info("ReportService: report_inventory_quantity is called.")
        user_name = await crud.report.get_user_name(self.db, user_id)
        list_result = await crud.report.report_inventory_quantity(self.db, tenant_id, branch)
        for row in list_result:
            print("product_id", row['product_id'])
            print("product_name", row['product_name'])
            print("total_quantity", row['total_quantity'])
            print("----------------------------------")
            
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
      
        print("html output", html_output)
        
        pdf = pdfkit.from_string(html_output, False)
        
        headers = {
            'Content-Disposition': f"attachment;filename=report-inventory-quantity.pdf"
        }
        
        logger.info("ReportService: report_inventory_quantity is called successfully.")
        return Response(content=pdf, headers=headers, media_type='application/pdf')
        
    async def gen_pdf(self, name: str):
        html = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
        <meta charset="UTF-8">
        <title>Báo cáo bán hàng</title>
        <style>
          table, th, td {
            border: 1px solid black;
            border-collapse: collapse;
          }
          th, td {
            padding: 5px;
            text-align: left;
          }
          th {
            background-color: #f2f2f2;
          }
        </style>
        </head>
        <body>

        <h2>Báo cáo bán hàng tháng 4</h2>

        <table>
          <tr>
            <th>Tên chi nhánh</th>
            <th>Tổng doanh số bán hàng</th>
            <th>Tổng lợi nhuận</th>
            <th>Thời gian</th>
          </tr>
          <tr>
            <td>Chi nhánh 1</td>
            <td>10.000.000đ</td>
            <td>7.000.000đ</td>
            <td>Tháng 4</td>
          </tr>
          <tr>
            <td>Chi nhánh 2</td>
            <td>12.500.000đ</td>
            <td>9.500.000đ</td>
            <td>Tháng 4</td>
          </tr>
        </table>

        <br>

        <h2>Chi tiết bán hàng chi nhánh 1</h2>

        <table>
          <tr>
            <th>Tên sản phẩm</th>
            <th>Số lượng bán</th>
            <th>Doanh thu</th>
            <th>Lợi nhuận</th>
            <th>Lượng hàng tồn kho</th>
            <th>Thời gian</th>
          </tr>
          <tr>
            <td>SP1</td>
            <td>150</td>
            <td>4.500.000đ</td>
            <td>3.500.000đ</td>
            <td>80</td>
            <td>Tháng 4</td>
          </tr>
          <tr>
            <td>SP2</td>
            <td>75</td>
            <td>5.500.000đ</td>
            <td>3.500.000đ</td>
            <td>15</td>
            <td>Tháng 4</td>
          </tr>
        </table>

        <br>

        <h2>Chi tiết bán hàng chi nhánh 2</h2>

        <table>
          <tr>
            <th>Tên sản phẩm</th>
            <th>Số lượng bán</th>
            <th>Doanh thu</th>
            <th>Lợi nhuận</th>
            <th>Lượng hàng tồn kho</th>
            <th>Thời gian</th>
          </tr>
          <tr>
            <td>SP1</td>
            <td>100</td>
            <td>8.000.000đ</td>
            <td>5.500.000đ</td>
            <td>15</td>
            <td>Tháng 4</td>
          </tr>
          <tr>
            <td>SP2</td>
            <td>50</td>
            <td>4.500.000đ</td>
            <td>4.500.000đ</td>
            <td>20</td>
            <td>Tháng 4</td>
          </tr>
        </table>

        </body>
        </html>

        """
        pdf = pdfkit.from_string(html, False)
        
        headers = {
            'Content-Disposition': f"attachment;filename={name}.pdf"
        }
        
        return Response(content=pdf, headers=headers, media_type='application/pdf')

