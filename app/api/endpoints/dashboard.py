from collections import OrderedDict
import logging

from typing import Annotated, Any, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from pydantic import UUID4
from datetime import date, datetime, timedelta

from app import crud
from app.api.depends import oauth2
# from app.api.depends.oauth2 import create_access_token, create_refresh_token, verify_refresh_token
from app.constant.app_status import AppStatus
from app.core.exceptions import error_exception_handler
from app.db.database import get_db
# from app.models import Dashboard
# from app.schemas import ChangePassword, DashboardResponse
# from app.schemas.dashboard import DashboardCreateParams, DashboardUpdate
from app.services.dashboard import DashboardService
from app.services.invoice_for_customer import InvoiceForCustomerService
from app.utils.response import make_response_object
from app.models import Employee

logger = logging.getLogger(__name__)
router = APIRouter()
import enum
class Period (str, enum.Enum):
    this_month ="Tháng này"
    last_month = "Tháng trước"
    today = "Hôm nay"
    yesterday = "Hôm qua"
    passed_7_days = "7 ngày qua"
class DateTime (str, enum.Enum):
    date = "Theo ngày"
    hour = "Theo giờ"
    day = "Theo thứ"

def get_today():
    today = datetime.now().date()
    return today, today

def get_yesterday():
    yesterday = datetime.now().date() - timedelta(days=1)
    return yesterday, yesterday

def get_last_7_days():
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=6)
    return start_date, end_date

def get_this_month():
    today = datetime.now()
    start_date = today.replace(day=1).date()
    end_date = today.date()
    return start_date, end_date

def get_last_month():
    today = datetime.now()
    first_day_this_month = today.replace(day=1)
    last_day_last_month = first_day_this_month - timedelta(days=1)
    first_day_last_month = last_day_last_month.replace(day=1)
    return first_day_last_month, last_day_last_month

@router.get("/dashboards")
async def get_total_sale_by_branch(
    branch: Optional[str] = None, # Quản lý thêm sản phẩm, vì không có chi nhánh làm việc nên cần truyền thêm muốn thêm ở chi nhánh nào
    datetime: Optional[DateTime] = None,
    period : Optional[Period] = None,
    user: Employee = Depends(oauth2.get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    current_user = await user
    if current_user.role == "Nhân viên":
        raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_ACCESS_DENIED)
    
    dashboard_service = DashboardService(db=db)
    logger.info("Endpoints: get_total_sale_by_branch called.")
    
    if current_user.branch:
        branch = current_user.branch
    else:
        branch = branch
        
    period_functions = {
        "Hôm nay": get_today,
        "Hôm qua": get_yesterday,
        "7 ngày qua": get_last_7_days,
        "Tháng này": get_this_month,
        "Tháng trước": get_last_month
    }
    start_date, end_date = period_functions[period]()
    
    # msg, dashboard_response = await dashboard_service.get_total_sale_by_branch(current_user.tenant_id, branch)

    if datetime == "Theo ngày":
        result,total_sale = await crud.invoice_for_customer.get_total_sale_by_branch(db=db,tenant_id=current_user.tenant_id,branch=branch,start_date=start_date,end_date=end_date) 
        response = {}
        for invoice in result:
            invoice_date = invoice.created_at.date()
            if invoice_date not in response:
                response[invoice_date] = invoice.total  # Initialize if the date doesn't exist in the response
            else:
                response[invoice_date] += invoice.total
        return {"data": response , "total": total_sale}
    
    elif datetime == "Theo giờ":
        result,total_sale = await crud.invoice_for_customer.get_total_sale_by_branch(db=db,tenant_id=current_user.tenant_id,branch=branch,start_date=start_date,end_date=end_date) 
        response = {}
        for invoice in result:
            invoice_time = invoice.created_at.time()
            hour_of_invoice = invoice_time.hour
            if hour_of_invoice not in response:
                response[f"{hour_of_invoice}h"] = invoice.total  
            else:
                response[hour_of_invoice] += invoice.total
     
        return {"data": response , "total": total_sale}
    
    elif datetime == "Theo thứ":
        result,total_sale = await crud.invoice_for_customer.get_total_sale_by_branch(db=db,tenant_id=current_user.tenant_id,branch=branch,start_date=start_date,end_date=end_date) 
        response = {}
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
       
        for invoice in result:
            invoice_date = invoice.created_at.date()
            day_of_week = invoice_date.weekday()
            day_name = days[day_of_week]
            if day_name not in response:
                response[day_name] = invoice.total  # Initialize if the date doesn't exist in the response
            else:
                response[day_name] += invoice.total
        return {"data": response , "total": total_sale}
        
    invoice_service = InvoiceForCustomerService(db=db)
    list_invoice = await invoice_service.get_all_invoice_for_customers(tenant_id=current_user.tenant_id, branch=branch)
    sum = 0
    for invoice in list_invoice[1]:
        sum += invoice.total
    
    logger.info("DashboardService: get_total_sale_by_id called successfully.")
    
    # msg, dashboard_response = await dashboard_service.get_total_sale_by_branch(tenant_id,branch)
    logger.info("Endpoints: get_total_sale_by_branch called successfully.")
    return {"sum": sum }

@router.get("/dashboards/sales_summary")
async def sales_summary(
    start_date: date,
    end_date: date,
    branch = None,
    user: Employee = Depends(oauth2.get_current_user),
    db: Session = Depends(get_db)    
):
    logger.info("DashboardEndpoint: sales_summary is called.")
    current_user = await user
    
    if branch:
        branch = branch
    else:
        branch = current_user.branch
    
    dashboard_service = DashboardService(db=db)
    
    res = await dashboard_service.sales_summary(start_date, end_date, current_user.tenant_id, branch)
    
    logger.info("DashboardEndpoint: sales_summary is called successfully.")
    
    return {"data": res}
