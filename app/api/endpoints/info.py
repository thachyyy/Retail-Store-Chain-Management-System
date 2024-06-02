import base64
from http.client import HTTPException
import logging

from typing import Annotated, Any, Optional
from fastapi import APIRouter, Depends, File, Query, UploadFile
from sqlalchemy.orm import Session
from pydantic import UUID4
from datetime import date

from app import crud
from app.api.depends import oauth2
# from app.api.depends.oauth2 import create_access_token, create_refresh_token, verify_refresh_token
from app.constant.app_status import AppStatus
from app.core.exceptions import error_exception_handler
from app.db.database import get_db
from app.models import Info
# from app.schemas import ChangePassword, InfoResponse
from app.schemas.info import InfoCreate, InfoUpdate
from app.services.import_order import ImportOrderService
from app.services.info import InfoService
from app.services.invoice_for_customer import InvoiceForCustomerService
from app.utils.response import make_response_object
from app.models import Employee
from uuid import uuid4
logger = logging.getLogger(__name__)
router = APIRouter()

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from app.core.s3 import S3ServiceSingleton  # Adjust the import based on your project structure


@router.post("/infos")
async def create_info(
    branch: Optional[str] = None, # Quản lý thêm sản phẩm, vì không có chi nhánh làm việc nên cần truyền thêm muốn thêm ở chi nhánh nào
    user: Employee = Depends(oauth2.get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    current_user = await user
    if current_user.role == "Nhân viên":
        raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_ACCESS_DENIED)
    
    info_service = InfoService(db=db)
    logger.info("Endpoints: create_info called.")
    
    if current_user.branch:
        branch = current_user.branch
    else:
        branch = branch

    msg, info_response = await info_service.create_info(current_user.tenant_id, branch)
    logger.info("Endpoints: create_info called successfully.")
    return make_response_object(info_response,msg)

@router.get("/infos/list")
async def get_list_infos(
    branch: Optional[str] = None,
    user: Employee = Depends(oauth2.get_current_user),
    db: Session = Depends(get_db)
):
    current_user = await user
    
    if current_user.branch:
        branch = current_user.branch
    else:
        branch = branch
        
    info_service = InfoService(db=db)
    msg, res = await info_service.get_info(
        tenant_id=current_user.tenant_id, 
        branch=branch, 
    )
    
    return make_response_object(res, msg)
@router.put("/infos/{info_id}")
async def update_info(
    product_id:str,
    tenant_id:str,
    sold :Optional[int]= None,
    sale_rate:Optional[float] = None,
    inventory:Optional[int]= None,
    category:Optional[str]= None,
    branch: Optional[str] = None,
    db: Session = Depends(get_db),
) -> Any:
    info_service = InfoService(db=db)
    invoice_for_customer_service = InvoiceForCustomerService(db=db)
    logger.info("Endpoints: update_info called.")
    current_product = await crud.info.get_info_id(product_id,tenant_id,branch,db)
    if sold:
        update_data = {
            "sold": (sold + current_product.sold),
            "inventory": (current_product.inventory - sold),
            }
    
    if inventory:
        flag = 0
        
        import_order_service = ImportOrderService(db=db)
        import_order_response = await import_order_service.get_all_import_orders(tenant_id=tenant_id,branch=branch)
        
        
        for import_order in import_order_response[1]:
            for item in import_order.list_import:
                if item.product_id == product_id:    
                    if flag == 1:
                        latest_batch =  import_order.created_at
                        # latest_import = batch.quantity
                        latest_import = item.quantity   
                        flag += 1
                    if flag == 0:
                        # Ngày nhập mới nhất
                        newest_batch = import_order.created_at
                        flag += 1
        
        sold_in_range = 0    
        
        if latest_batch:
            invoice_in_range =  await invoice_for_customer_service.get_all_invoice_for_customers(tenant_id=tenant_id, branch=branch,start_date_1=latest_batch,end_date_1=newest_batch)
            for invoice in invoice_in_range[1]:
                for item in invoice.order_detail:
                    if item.product_id == product_id:
                        sold_in_range += item.quantity

        if sold_in_range >= latest_import:    
            sell_rate = 100
        else:    
            if latest_import > 0:
                sell_rate = (sold_in_range / latest_import )*100
            else: 
                sell_rate = 0
        if sold_in_range == 0:
            sell_rate = 0 
        update_data = {
            "inventory": (inventory + current_product.inventory),
            "sale_rate": round(sell_rate,2)
            }    
    print("lisstst",list)
    info_update = InfoUpdate(**update_data)
    # sold += current_product.sold
    msg, info_response = await info_service.update_info(product_id=product_id, obj_in=info_update, tenant_id=tenant_id, branch=branch)
    
    logger.info("Endpoints: update_info called successfully.")
    return make_response_object(info_response, msg)

# @router.get("/infos")
# async def get_all_infos(
#     limit: Optional[int] = None,
#     offset:Optional[int] = None,
#     status: Optional[str] = None,
#     low_price: Optional[int] = None,
#     high_price: Optional[int] = None,
#     categories: Optional[str] = None,
#     query_search: Optional[str] = None,
#     branch: Optional[str] = None,
#     db: Session = Depends(get_db),
#     user: Employee = Depends(oauth2.get_current_user),
# ) -> Any:
    
#     current_user = await user
    
#     if branch:
#         branch = branch
#     else:
#         branch = current_user.branch
    
#     info_service = InfoService(db=db)
#     logger.info("Endpoints: get_all_infos called.")
#     msg,info_response= await info_service.get_all_infos(current_user.tenant_id, branch, limit,offset,status,low_price,high_price,categories,query_search)
    
#     logger.info("Endpoints: get_all_infos called successfully.")
#     return make_response_object(info_response, msg)

# @router.get("/infos/{info_id}")
# async def get_info_by_id(
#     info_id: str, 
#     db: Session = Depends(get_db),
#     branch: Optional[str] = None,
#     user: Employee = Depends(oauth2.get_current_user),
# ) -> Any:
#     current_user = await user
    
#     if branch:
#         branch = branch
#     else:
#         branch = current_user.branch
    
#     info_service = InfoService(db=db)
    
#     logger.info("Endpoints: get_info_by_id called.")  
#     msg, info_response = await info_service.get_info_by_id(current_user.tenant_id, branch, info_id)
#     logger.info("Endpoints: get_all_infos called successfully.")
#     return make_response_object(info_response, msg)

# @router.get("/infos/barcode/{barcode}")
# async def get_info_by_barcode(
#     barcode: str, 
#     db: Session = Depends(get_db),
#     branch: Optional[str] = None,
#     user: Employee = Depends(oauth2.get_current_user),
# ) -> Any:
#     current_user = await user
    
#     if branch:
#         branch = branch
#     else:
#         branch = current_user.branch
    
#     info_service = InfoService(db=db)
    
#     logger.info("Endpoints: get_info_by_id called.")  
#     msg, info_response = await info_service.get_info_by_barcode(barcode, current_user.tenant_id, branch)
#     logger.info("Endpoints: get_all_infos called successfully.")
#     return make_response_object(info_response, msg)
     


# @router.delete("/infos/{info_id}")
# async def delete_info(
#     info_id: str, 
#     db: Session = Depends(get_db),
#     branch: Optional[str] = None,
#     user: Employee = Depends(oauth2.get_current_user),
# ) -> Any:
    
#     current_user = await user
#     if current_user.role == "Nhân viên":
#         raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_ACCESS_DENIED)
    
#     if branch:
#         branch = branch
#     else:
#         branch = current_user.branch
    
#     info_service = InfoService(db=db)
    
#     logger.info("Endpoints: delete_info called.")
#     msg, info_response = await info_service.delete_info(info_id, current_user.tenant_id, branch)
#     logger.info("Endpoints: delete_info called successfully.")
#     return make_response_object(info_response, msg)


