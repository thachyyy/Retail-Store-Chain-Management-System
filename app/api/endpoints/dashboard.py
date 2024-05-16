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
from app.services.batch import BatchService
from app.services.dashboard import DashboardService
from app.services.invoice_for_customer import InvoiceForCustomerService
from app.services.product import ProductService
from app.utils.response import make_response_object
from app.models import Employee

import time

logger = logging.getLogger(__name__)
router = APIRouter()
import enum
class Period (str, enum.Enum):
    today = "Hôm nay"
    seven_days = "7 ngày"
    thirty_days ="30 ngày"
    ninety_days ="90 ngày"
    this_year = "Năm nay"
    
class DateTime (str, enum.Enum):
    date = "Theo ngày"
    hour = "Theo giờ"
    day = "Theo thứ"
    month = "Theo tháng"
class Sort_list(str, enum.Enum):
    quantity = "Theo số lượng"
    sale = "Theo doanh thu"

def get_today():
    today = datetime.now().date()
    return today, today

def get_yesterday():
    yesterday = datetime.now().date() - timedelta(days=1)
    return yesterday, yesterday

def get_7_days():
    end_date = datetime.now().date() - timedelta(days=1)
    start_date = end_date - timedelta(days=6)
    return start_date, end_date

def get_last_7_days():
    start_date, end_date = get_7_days()
    start_date = start_date - timedelta(days=7)
    end_date = start_date + timedelta(days=6)
    return start_date, end_date

def get_30_days():
    end_date = datetime.now().date() - timedelta(days=1)
    start_date = end_date - timedelta(days=29)
    return start_date,end_date

def get_last_30_days():
    start_date, end_date = get_30_days()
    start_date = start_date - timedelta(days=30)
    end_date = start_date + timedelta(days=29)
    return start_date, end_date

def get_90_days():
    end_date = datetime.now().date() - timedelta(days=1)
    start_date = end_date - timedelta(days=89)
    return start_date,end_date

def get_last_90_days():
    start_date,end_date = get_90_days()
    start_date = start_date - timedelta(days=90)
    end_date = start_date + timedelta(days=89)
    return start_date, end_date
def get_this_year():
    today = datetime.now().date()
    current_year = datetime.now().year

    first_day_of_year = datetime(current_year, 1, 1)
    return first_day_of_year,today
def get_last_year():

    last_year = datetime.now().year - 1

    first_day_of_last_year = datetime(last_year, 1, 1)
    last_day_of_last_year = datetime(last_year, 12, 31)
    
    return first_day_of_last_year,last_day_of_last_year
@router.get("/dashboard/get_total_sale_by_branch")
async def get_total_sale_by_branch(
    branch: Optional[str] = None, # Quản lý thêm sản phẩm, vì không có chi nhánh làm việc nên cần truyền thêm muốn thêm ở chi nhánh nào
    date_time: Optional[DateTime] = None,
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
        "7 ngày": get_7_days,
        "30 ngày" : get_30_days,
        "90 ngày": get_90_days,
        "Năm nay": get_this_year
    }
    response = {}
    response_1 = {}  
    hours = ['0h', '1h', '2h', '3h', '4h', '5h', '6h', '7h', '8h', '9h', '10h', '11h', '12h', '13h', '14h', '15h', '16h', '17h', '18h', '19h', '20h', '21h', '22h', '23h']
    today = datetime.now()
    if period == "Hôm nay":
        start_date, end_date = period_functions[period]()
        result,total_sale = await crud.invoice_for_customer.get_total_sale_by_branch(db=db,tenant_id=current_user.tenant_id,branch=branch,start_date=start_date,end_date=end_date) 
        
        start_date, end_date = get_yesterday()
        result_1,total_sale_1 = await crud.invoice_for_customer.get_total_sale_by_branch(db=db,tenant_id=current_user.tenant_id,branch=branch,start_date=start_date,end_date=end_date) 
        
    elif period == "7 ngày": 
        
        start_date, end_date = period_functions[period]()
        result,total_sale = await crud.invoice_for_customer.get_total_sale_by_branch(db=db,tenant_id=current_user.tenant_id,branch=branch,start_date=start_date,end_date=end_date)
        
        start_date, end_date = get_last_7_days()
        result_1,total_sale_1 = await crud.invoice_for_customer.get_total_sale_by_branch(db=db,tenant_id=current_user.tenant_id,branch=branch,start_date=start_date,end_date=end_date)
    
    elif period == "30 ngày":
        
        start_date, end_date = period_functions[period]()   
        result,total_sale = await crud.invoice_for_customer.get_total_sale_by_branch(db=db,tenant_id=current_user.tenant_id,branch=branch,start_date=start_date,end_date=end_date)
        
        start_date, end_date = get_last_30_days()
        result_1,total_sale_1= await crud.invoice_for_customer.get_total_sale_by_branch(db=db,tenant_id=current_user.tenant_id,branch=branch,start_date=start_date,end_date=end_date)
        
    elif period == "90 ngày":
        
        start_date, end_date = period_functions[period]()
        result,total_sale = await crud.invoice_for_customer.get_total_sale_by_branch(db=db,tenant_id=current_user.tenant_id,branch=branch,start_date=start_date,end_date=end_date)
        
        start_date, end_date = get_last_90_days()
        result_1,total_sale_1 = await crud.invoice_for_customer.get_total_sale_by_branch(db=db,tenant_id=current_user.tenant_id,branch=branch,start_date=start_date,end_date=end_date)
    
    elif period == "Năm nay":
        
        start_date, end_date = period_functions[period]()
        result,total_sale = await crud.invoice_for_customer.get_total_sale_by_branch(db=db,tenant_id=current_user.tenant_id,branch=branch,start_date=start_date,end_date=end_date)
        
        start_date, end_date = get_last_year()
        result_1,total_sale_1 = await crud.invoice_for_customer.get_total_sale_by_branch(db=db,tenant_id=current_user.tenant_id,branch=branch,start_date=start_date,end_date=end_date)
        
    
    # # msg, dashboard_response = await dashboard_service.get_total_sale_by_branch(current_user.tenant_id, branch)
    # print("date_timeeee",date_time)
    if date_time == "Theo ngày": 
          
        if period == "7 ngày":
            today = today - timedelta(days=7)
            for i in range(7):
                date = today + timedelta(days=i)
                response[date.strftime('%Y-%m-%d')] = 0  
                
            last_7_days = today - timedelta(days=7)
            for i in range(7):
                date = last_7_days + timedelta(days=i)
                response_1[date.strftime('%Y-%m-%d')] = 0
        elif period == "30 ngày":  
            today = today - timedelta(days=30)
            for i in range(30):
                date = today + timedelta(days=i)
                response[date.strftime('%Y-%m-%d')] = 0  
                
            last_30_days = today - timedelta(days=30)
            for i in range(30):
                date = last_30_days + timedelta(days=i)
                response_1[date.strftime('%Y-%m-%d')] = 0 
        elif period == "90 ngày":    
            today = today - timedelta(days=90)
            for i in range(90):
                date = today + timedelta(days=i)
                response[date.strftime('%Y-%m-%d')] = 0  
                
            last_30_days = today - timedelta(days=90)
            for i in range(90):
                date = last_30_days + timedelta(days=i)
                response_1[date.strftime('%Y-%m-%d')] = 0                 
        elif period == "Hôm nay":
            response[today.strftime('%Y-%m-%d')] = 0  
            yesterday = today - timedelta(days=1)
            response_1[yesterday.strftime('%Y-%m-%d')] = 0                   
        for invoice in result:
            invoice_date = invoice.created_at.date()
            response[f'{invoice_date}'] += invoice.total
            
        for invoice in result_1:
            invoice_date = invoice.created_at.date()
            response_1[f'{invoice_date}'] += invoice.total
                
    elif date_time == "Theo giờ":
        for i in range(24):
            response[hours[i]] = 0
            response_1[hours[i]] = 0
            
        for invoice in result:
            invoice_time = invoice.created_at.time()
            hour_of_invoice = invoice_time.hour
            response[f'{hour_of_invoice}h'] += invoice.total
     
        for invoice in result_1:
            invoice_time = invoice.created_at.time()
            hour_of_invoice = invoice_time.hour
            # if hour_of_invoice not in response_1:
            #     response_1[f"{hour_of_invoice}h"] = invoice.total  
            # else:
            
            response[f'{hour_of_invoice}h'] += invoice.total
                
    elif date_time == "Theo thứ":
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        for i in range(7):
            response[days[i]] = 0
            response_1[days[i]] = 0
            
        for invoice in result:
            invoice_date = invoice.created_at.date()
            day_of_week = invoice_date.weekday()
            day_name = days[day_of_week]
            # if day_name not in response:
            #     response[day_name] = invoice.total  # Initialize if the date doesn't exist in the response
            # else:
            response[day_name] += invoice.total
        
        for invoice in result_1:
            invoice_date = invoice.created_at.date()
            day_of_week = invoice_date.weekday()
            day_name = days[day_of_week]
            # if day_name not in response_1:
            #     response_1[day_name] = invoice.total  # Initialize if the date doesn't exist in the response
            # else:
            response_1[day_name] += invoice.total    
                    
    elif date_time == "Theo tháng":
        months = ["January", "February", "March", "April", "May", "June", 
          "July", "August", "September", "October", "November", "December"]
        for i in range(12):
            response[months[i]] = 0
            response_1[months[i]] = 0
            
        for invoice in result:
            invoice_date = invoice.created_at
            month_today = invoice_date.month - 1
            month = months[month_today]
            # if month not in response:
            #     response[month] = invoice.total  # Initialize if the date doesn't exist in the response
            # else:
            response[month] += invoice.total
                
        for invoice in result_1:
            invoice_date = invoice.created_at
            month_today = invoice_date.month - 1
            month = months[month_today]
            # if month not in response_1:
            #     response_1[month] = invoice.total  # Initialize if the date doesn't exist in the response
            # else:
            response_1[month] += invoice.total  
    
    return {"data": response, "data_1": response_1, "total_sale": total_sale}

@router.get("/dashboard/get_top_10_branch_by_total_sale")
async def get_top_10_branch_by_total_sale(
    start_date: date,
    end_date: date,
    branch: Optional[str] = None, # Quản lý thêm sản phẩm, vì không có chi nhánh làm việc nên cần truyền thêm muốn thêm ở chi nhánh nào
    # period : Optional[Period] = None,
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
        
    # period_functions = {
    #     "Hôm nay": get_today,
    #     "Hôm qua": get_yesterday,
    #     "7 ngày qua": get_last_7_days,
    #     "Tháng này": get_this_month,
    #     "Tháng trước": get_last_month
    # }
    # start_date, end_date = period_functions[period]()
    

    result,total_sale = await crud.invoice_for_customer.get_total_sale_by_all_branch(db=db,tenant_id=current_user.tenant_id,start_date=start_date,end_date=end_date) 
   
    response = {}
    for branch in result:
        total_purchase_order = await  crud.purchase_order.get_total_purchase_order_by_all_branch(db=db,tenant_id=current_user.tenant_id,branch=branch.branch,start_date=start_date,end_date=end_date) 
        if branch.branch not in response:
            response[branch.branch] = {
                "total_sale": branch.total,
                "total_purchase_order": total_purchase_order
                }
        else:
            response[branch.branch]["total_sale"] += branch.total
            # response[branch.branch]["total_purchase_order"] += total_purchase_order
    return {"data": response}
    
@router.get("/dashboard/get_top_10_product_by_total_sale")
async def get_top_10_product_by_total_sale(
    branch: Optional[str] = None, # Quản lý thêm sản phẩm, vì không có chi nhánh làm việc nên cần truyền thêm muốn thêm ở chi nhánh nà
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
        "7 ngày": get_7_days,
        "30 ngày" : get_30_days,
        "90 ngày": get_90_days,
        "Năm nay": get_this_year
    }
    start_date, end_date = period_functions[period]()
    
    # msg, dashboard_response = await dashboard_service.get_total_sale_by_branch(current_user.tenant_id, branch)
    product_service = ProductService(db=db)
    logger.info("Endpoints: get_all_products called.")
    product_response = await product_service.get_all_products(current_user.tenant_id, branch)
    list_product = []
    for product in product_response[1]:
        if product.product_name not in list_product:
            list_product += [product.product_name]
      # Using list comprehension for clarity

    # Initialize response dictionary
    response = {}
    invoice_for_customer_service = InvoiceForCustomerService(db=db)
    # Fetch all invoices once to improve efficiency
    list_invoice = await invoice_for_customer_service.get_all_invoice_for_customers(tenant_id=current_user.tenant_id, branch=branch,start_date=start_date,end_date=end_date)

    # Accumulate data
    for invoice in list_invoice[1]:
        for order_detail in invoice.order_detail:
            product_name = order_detail.product_name
            if product_name in list_product:
                if product_name not in response:
                    # Initialize the dictionary if it doesn't exist
                    response[product_name] = {
                        "sales_total": order_detail.price * order_detail.quantity,
                        "sold": order_detail.quantity
                    }
                else:
                    # Update the dictionary if it already exists
                    response[product_name]['sales_total'] += order_detail.price * order_detail.quantity
                    response[product_name]['sold'] += order_detail.quantity
   
    products = [(name, details['sales_total'], details['sold']) for name, details in response.items()]  
    products_sorted_by_sales = sorted(products, key=lambda x: x[1], reverse=True)
    top_10_products = products_sorted_by_sales[:10]
    result = []
    for product in top_10_products:
        result.append({
            "product": product[0],
            "sales_total": product[1],
            "order_total": product[2]
        })
    return {"data":result}

@router.get("/dashboard/sales_summary")
async def sales_summary(
    start_date: date,
    end_date: date,
    branch = None,
    user: Employee = Depends(oauth2.get_current_user),
    db: Session = Depends(get_db)    
):
    logger.info("DashboardEndpoint: sales_summary is called.")
    current_user = await user
    
    if current_user.role == "Nhân viên":
        raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_ACCESS_DENIED)
    
    if branch:
        branch = branch
    else:
        branch = current_user.branch
    
    dashboard_service = DashboardService(db=db)
    
    res = await dashboard_service.sales_summary(start_date, end_date, current_user.tenant_id, branch)
    
    return res
    
@router.get("/dashboard/get_all_sell_through_rate")
async def get_all_sell_through_rate(
    branch: Optional[str] = None,
    limit: Optional[int] = None,
    offset : Optional[int] = None,
    user: Employee = Depends(oauth2.get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    
    # start_time = time.time()
    
    current_user = await user
    if current_user.role == "Nhân viên":
        raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_ACCESS_DENIED)
    if branch:
        branch = branch
    else:
        branch = current_user.branch
        
    dashboard_service = DashboardService(db=db)
    
    product_service = ProductService(db=db)
    logger.info("Endpoints: get_all_products called.")
    product_response= await product_service.get_all_products(current_user.tenant_id, branch)
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
    invoice_for_customer_service = InvoiceForCustomerService(db=db)   
    result = []
    flag = 0
    latest_batch = datetime.now()
    for id in list_product:
        inventory = 0
        sales_total = 0
        sold = 0
        product = await crud.product.get_product_by_id(db=db,tenant_id=current_user.tenant_id,branch=branch,product_id=id)
        batch_service = BatchService(db=db)
        
        # Danh sách Lô theo thứ tự Lô mới nhất -> cũ nhất
        batch_response = await batch_service.get_all_batches(tenant_id=current_user.tenant_id,
            branch=branch,
            limit=limit, 
            offset=offset,
            query_search = id)
        
       
        
        latest_import = 0
        for batch in batch_response[1]:
            if flag == 1:
                latest_batch =  batch.created_at
                latest_import = batch.quantity
                
            if flag == 0:
                # Ngày nhập mới nhất
                newest_batch = batch.created_at
                flag += 1
            
           
            inventory += batch.quantity
        # list_invoice_in_= await invoice_for_customer_service.get_all_invoice_for_customers(tenant_id=current_user.tenant_id, branch=branch, start_date=latest_batch,end_date=)
         
        list_invoice = await invoice_for_customer_service.get_all_invoice_for_customers(tenant_id=current_user.tenant_id, branch=branch)
        
        for invoice in list_invoice[1]:
            for order_detail in invoice.order_detail:
                if order_detail.product_id == id:
                    sales_total += order_detail.price * order_detail.quantity
                    sold += order_detail.quantity
        # print("product_name",product.product_name)
        # print("sale_price",product.sale_price)
        # print("inventory",inventory)
        # print("sales_total",sales_total)
        # print("sold",sold)
 
        sold_in_range = 0    
        if latest_batch:
            invoice_in_range =  await invoice_for_customer_service.get_all_invoice_for_customers(tenant_id=current_user.tenant_id, branch=branch,start_date=latest_batch,end_date=newest_batch)
        for invoice in invoice_in_range[1]:
            for order_detail in invoice.order_detail:
                if order_detail.product_id == id:
                    sold_in_range += order_detail.quantity
        if latest_import > 0:
            # print("sold_in_range",sold_in_range)
            # print("latest_import",latest_import)
            sell_rate = (sold_in_range / (latest_import+sold))*100
        else: 
            sell_rate = 0
            
        new_item = {
            "product_name": product.product_name,
            "sale_price": product.sale_price,
            "inventory": inventory,
            "sales_total": sales_total,
            "sold": sold,
            "sell_rate": sell_rate
        }
        for item in result:
            if item["product_name"] == new_item["product_name"]: 
                item['sale_price'] += new_item["sale_price"]
                item['sales_total'] += new_item["sales_total"]
                item['inventory'] += new_item["inventory"]
                item['sold'] += new_item["sold"]
                item['sell_rate'] += new_item["sell_rate"]
                break
        else:    
            result.append(new_item)
        # dashboard_service = DashboardService(db=db)
        # list_sales_by_product = await dashboard_service.sales_report_by_product(current_user.tenant_id,branch)
        
    
    return {"data":result} 

@router.get("/dashboard/top_10_sell_through_rate")
async def get_top_10_sell_through_rate(
    branch: Optional[str] = None,
    user: Employee = Depends(oauth2.get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    
    start_time = time.time()
    
    current_user = await user
    if current_user.role == "Nhân viên":
        raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_ACCESS_DENIED)
    if branch:
        branch = branch
    else:
        branch = current_user.branch
        
        
    invoice_for_customer_service = InvoiceForCustomerService(db=db)
    
    
    product_service = ProductService(db=db)
    logger.info("Endpoints: get_all_products called.")
    product_response= await product_service.get_all_products(current_user.tenant_id, branch)
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
    
    result = []
    flag = 0
    latest_batch = datetime.now()
    for id in list_product:
        inventory = 0
        sales_total = 0
        sold = 0
        product = await crud.product.get_product_by_id(db=db,tenant_id=current_user.tenant_id,branch=branch,product_id=id)
        batch_service = BatchService(db=db)
        
        # Danh sách Lô theo thứ tự Lô mới nhất -> cũ nhất
        batch_response = await batch_service.get_all_batches(tenant_id=current_user.tenant_id,
            branch=branch,
            query_search = id)
        
       
        
        latest_import = 0
        for batch in batch_response[1]:
            if flag == 1:
                latest_batch =  batch.created_at
                latest_import = batch.quantity
                
            if flag == 0:
                # Ngày nhập mới nhất
                newest_batch = batch.created_at
                flag += 1
            
            print("latest_batchhhh",latest_batch)
            print("newest_batchhhh",newest_batch)
            inventory += batch.quantity
        # list_invoice_in_= await invoice_for_customer_service.get_all_invoice_for_customers(tenant_id=current_user.tenant_id, branch=branch, start_date=latest_batch,end_date=)
            
        list_invoice = await invoice_for_customer_service.get_all_invoice_for_customers(tenant_id=current_user.tenant_id, branch=branch,start_date=latest_batch,end_date=newest_batch)
        
        for invoice in list_invoice[1]:
            for order_detail in invoice.order_detail:
                if order_detail.product_id == id:
                    sales_total += order_detail.price * order_detail.quantity
                    sold += order_detail.quantity
        # print("product_name",product.product_name)
        # print("sale_price",product.sale_price)
        # print("inventory",inventory)
        # print("sales_total",sales_total)
        # print("sold",sold)
        sold_in_range = 0    
        if latest_batch:
            invoice_in_range =  await invoice_for_customer_service.get_all_invoice_for_customers(tenant_id=current_user.tenant_id, branch=branch,start_date=latest_batch,end_date=newest_batch)
        for invoice in invoice_in_range[1]:
            for order_detail in invoice.order_detail:
                if order_detail.product_id == id:
                    sold_in_range += order_detail.quantity
        if latest_import > 0:
            # print("sold_in_range",sold_in_range)
            # print("latest_import",latest_import)
            sell_rate = (sold_in_range / (latest_import+sold))*100
        else: 
            sell_rate = 0
            
        new_item = {
            "product_name": product.product_name,
            "sale_price": product.sale_price,
            "inventory": inventory,
            "sales_total": sales_total,
            "sold": sold,
            "sell_rate": round(sell_rate,2)
        }
        for item in result:
            if item["product_name"] == new_item["product_name"]: 
                item['sale_price'] += new_item["sale_price"]
                item['sales_total'] += new_item["sales_total"]
                item['inventory'] += new_item["inventory"]
                item['sold'] += new_item["sold"]
                item['sell_rate'] += new_item["sell_rate"]
                break
        else:    
            result.append(new_item)
        # dashboard_service = DashboardService(db=db)
        # list_sales_by_product = await dashboard_service.sales_report_by_product(current_user.tenant_id,branch)
        
    end_time = time.time()
    elapsed_time = end_time - start_time
    print ("elapsed_time:{0}".format(elapsed_time) + "[sec]")
    top_ten_products = sorted(result, key=lambda x: x['sell_rate'], reverse=True)[:10]
    return {"data":top_ten_products}  
 





    
# @router.get("/dashboard/sales_summary")
# async def sales_summary(
#     start_date: date,
#     end_date: date,
#     branch = None,
#     user: Employee = Depends(oauth2.get_current_user),
#     db: Session = Depends(get_db)    
# ):
#     logger.info("DashboardEndpoint: sales_summary is called.")
#     current_user = await user
    
#     if branch:
#         branch = branch
#     else:
#         branch = current_user.branch
    
#     dashboard_service = DashboardService(db=db)
    
#     res = await dashboard_service.sales_summary(start_date, end_date, current_user.tenant_id, branch)
    
#     logger.info("DashboardEndpoint: sales_summary is called successfully.")
    
#     return {"data": res}
