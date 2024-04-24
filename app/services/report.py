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

logger = logging.getLogger(__name__)

class ReportService:
    def __init__(self, db: Session):
        self.db = db
        
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
