import logging

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Any, Optional

from app import crud
from app.db.database import get_db
from app.api.depends import oauth2
from app.constant.app_status import AppStatus
from app.core.exceptions import error_exception_handler
from app.schemas.report import InventoryItem
from app.services.invoice_for_customer import InvoiceForCustomerService
from app.services.product import ProductService
from app.services.report import ReportService
from app.utils.response import make_response_object
# from app.schemas.vendor import VendorCreateParams, VendorUpdate
from app.models import Employee

from fastapi import FastAPI, Response
from fastapi.responses import StreamingResponse
import pdfkit
from starlette.responses import FileResponse
from fastapi.responses import Response
from datetime import date, datetime

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/report/abc_analysis")
async def sales_summary(
    start_date: date,
    end_date: date,
    branch: Optional[str] = None,
    user: Employee = Depends(oauth2.get_current_user),
    db: Session = Depends(get_db)    
):
    current_user = await user
    if current_user.role == "Nhân viên":
        raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_ACCESS_DENIED)
    if branch:
        branch = branch
    else:
        branch = current_user.branch
    
    report_service = ReportService(db=db) 
    product_service = ProductService(db=db)
    logger.info("Endpoints: get_all_products called.")
    product_response = await product_service.get_all_products(current_user.tenant_id, branch)
    list_product = []
   
    
    for product in product_response[1]:
        if product.id not in list_product:
            list_product += [product.id]
    
    result = []
    for id in list_product:        
        sold = 0
        product = await crud.product.get_product_by_id(db=db,tenant_id=current_user.tenant_id,branch=branch,product_id=id)
        
        invoice_for_customer_service = InvoiceForCustomerService(db=db)    
        
        list_invoice = await invoice_for_customer_service.get_all_invoice_for_customers(tenant_id=current_user.tenant_id, branch=branch,start_date=start_date,end_date=end_date)
        
        
        for invoice in list_invoice[1]:
            for order_detail in invoice.order_detail:
                if order_detail.product_id == id:
                    sold += order_detail.quantity
                    
                    
        new_item = {
                "product_name": product.product_name,
                "sale_price": product.sale_price,
                "sold": sold,
            }        
        
        for item in result:
            if item["product_name"] == new_item["product_name"]: 
                item['sold'] += new_item["sold"]
                break
        else:    
            result.append(new_item)
    # inventory_items = [InventoryItem(**item) for item in result]

    response = await report_service.abc_analysis(start_date,end_date,result,current_user.id, current_user.tenant_id, branch)
    return response

@router.get("/report/fsn_analysis")
async def sales_summary(
    start_date: date,
    end_date: date,
    branch: Optional[str] = None,
    user: Employee = Depends(oauth2.get_current_user),
    db: Session = Depends(get_db)    
):
    current_user = await user
    if current_user.role == "Nhân viên":
        raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_ACCESS_DENIED)
    if branch:
        branch = branch
    else:
        branch = current_user.branch
    
    report_service = ReportService(db=db) 
    product_service = ProductService(db=db)
    logger.info("Endpoints: get_all_products called.")
    product_response = await product_service.get_all_products(current_user.tenant_id, branch)
    list_product = []
   
    for product in product_response[1]:
        if product.id not in list_product:
            list_product += [product.id]
    
    result = []
    for id in list_product:        
        sold = 0
        product = await crud.product.get_product_by_id(db=db,tenant_id=current_user.tenant_id,branch=branch,product_id=id)
        
        invoice_for_customer_service = InvoiceForCustomerService(db=db)    
        
        list_invoice = await invoice_for_customer_service.get_all_invoice_for_customers(tenant_id=current_user.tenant_id, branch=branch,start_date=start_date,end_date=end_date)
        
        
        for invoice in list_invoice[1]:
            for order_detail in invoice.order_detail:
                if order_detail.product_id == id:
                    sold += order_detail.quantity
                    
        new_item = {
                "product_name": product.product_name,
                "sale_price": product.sale_price,
                "sold": sold
            }        
        
        for item in result:
            if item["product_name"] == new_item["product_name"]: 
                item['sold'] += new_item["sold"]
                break
        else:    
            result.append(new_item)
    
    inventory_items = [InventoryItem(**item) for item in result]

    response = await report_service.fsn_analysis(inventory_items,start_date,end_date,current_user.id, current_user.tenant_id, branch)
    return response        


@router.get("/report/inventory_quantity")
async def report_inventory_quantity(
    branch: str = None,
    user: Employee = Depends(oauth2.get_current_user),
    db: Session = Depends(get_db)
):
    current_user = await user
    
    if current_user.role == "Nhân viên":
        raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_ACCESS_DENIED)
    
    if branch:
        branch = branch
    else:
        branch= current_user.branch
        
    report_service = ReportService(db=db)
    res = await report_service.report_inventory_quantity(current_user.id, current_user.tenant_id, branch)
    
    return res

@router.get("/report/sales_by_branch")
async def sales_report_by_branch(
    start_date: date,
    end_date: date,
    user: Employee = Depends(oauth2.get_current_user),
    db: Session = Depends(get_db)
):
    current_user = await user
    if current_user.role != "Quản lý":
        raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_ACCESS_DENIED)
    
    report_service = ReportService(db=db)
    res = await report_service.sales_report_by_branch(current_user.id, start_date, end_date, current_user.tenant_id)
    
    return res

@router.get("/report/sales_by_product")
async def sales_report_by_product(
    start_date: date,
    end_date: date,
    branch: str = None,
    user: Employee = Depends(oauth2.get_current_user),
    db: Session = Depends(get_db)
):
    current_user = await user
    if current_user.role == "Nhân viên":
        raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_ACCESS_DENIED)
    
    report_service = ReportService(db=db)
    
    # Kiểm tra trường hợp branch == all thì lấy thông tin toàn bộ các chi nhánh
    # Todo here
    if branch:
        branch = branch
    else:
        branch = current_user.branch
    
    res = await report_service.sales_report_by_product(current_user.id, start_date, end_date, current_user.tenant_id, branch)
    
    return res

@router.get("/report/sales_by_customer")
async def sales_report_by_customer(
    start_date: date,
    end_date: date,
    branch: str = None,
    user: Employee = Depends(oauth2.get_current_user),
    db: Session = Depends(get_db)
):
    current_user = await user
    if current_user.role == "Nhân viên":
        raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_ACCESS_DENIED)
    
    report_service = ReportService(db=db)
    
    # Kiểm tra trường hợp branch == all thì lấy thông tin toàn bộ các chi nhánh
    # Todo here
    if branch:
        branch = branch
    else:
        branch = current_user.branch
    
    res = await report_service.sales_report_by_customer(current_user.id, start_date, end_date, current_user.tenant_id, branch)
    
    return res

@router.get("/report/sales_by_categories")
async def sales_report_by_categories(
    start_date: date,
    end_date: date,
    branch: str = None,
    user: Employee = Depends(oauth2.get_current_user),
    db: Session = Depends(get_db)
):
    current_user = await user
    if current_user.role == "Nhân viên":
        raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_ACCESS_DENIED)
    
    report_service = ReportService(db=db)
    
    # Kiểm tra trường hợp branch == all thì lấy thông tin toàn bộ các chi nhánh
    # Todo here
    if branch:
        branch = branch
    else:
        branch = current_user.branch
    
    res = await report_service.sales_report_by_categories(current_user.id, start_date, end_date, current_user.tenant_id, branch)
    
    return res