import logging

from typing import Annotated, Any, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from pydantic import UUID4
from datetime import date

from app.api.depends import oauth2
# from app.api.depends.oauth2 import create_access_token, create_refresh_token, verify_refresh_token
from app.constant.app_status import AppStatus
from app.core.exceptions import error_exception_handler
from app.db.database import get_db
from app.models import Product
# from app.schemas import ChangePassword, ProductResponse
from app.schemas.product import ProductCreateParams, ProductUpdate
from app.services.product import ProductService
from app.utils.response import make_response_object
from app.models import Employee

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/products")
async def create_product(
    product_create: ProductCreateParams,
    branch: Optional[str] = None, # Quản lý thêm sản phẩm, vì không có chi nhánh làm việc nên cần truyền thêm muốn thêm ở chi nhánh nào
    user: Employee = Depends(oauth2.get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    current_user = await user
    if current_user.role == "Nhân viên":
        raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_ACCESS_DENIED)
    
    product_service = ProductService(db=db)
    logger.info("Endpoints: create_product called.")
    
    if current_user.branch:
        branch_name_detail = current_user.branch
    else:
        branch_name_detail = branch
    
    msg, product_response = await product_service.create_product(product_create, current_user.tenant_id, branch_name_detail)
    logger.info("Endpoints: create_product called successfully.")
    return make_response_object(product_response,msg)

@router.get("/products")
async def get_all_products(
    limit: Optional[int] = None,
    offset:Optional[int] = None,
    status: Optional[str] = None,
    low_price: Optional[int] = None,
    high_price: Optional[int] = None,
    categories: Optional[str] = None,
    query_search: Optional[str] = None,
    db: Session = Depends(get_db)
) -> Any:
    product_service = ProductService(db=db)
    logger.info("Endpoints: get_all_products called.")
    msg,product_response= await product_service.get_all_products(limit,offset,status,low_price,high_price,categories,query_search)
    
    logger.info("Endpoints: get_all_products called successfully.")
    return make_response_object(product_response, msg)

@router.get("/products/{product_id}")
async def get_product_by_id(product_id: str, db: Session = Depends(get_db)) -> Any:
    product_service = ProductService(db=db)
    
    logger.info("Endpoints: get_product_by_id called.")  
    msg, product_response = await product_service.get_product_by_id(product_id)
    logger.info("Endpoints: get_all_products called successfully.")
    return make_response_object(product_response, msg)

@router.get("/products/barcode/{barcode}")
async def get_product_by_barcode(barcode: str, db: Session = Depends(get_db)) -> Any:
    product_service = ProductService(db=db)
    
    logger.info("Endpoints: get_product_by_id called.")  
    msg, product_response = await product_service.get_product_by_barcode(barcode)
    logger.info("Endpoints: get_all_products called successfully.")
    return make_response_object(product_response, msg)
     
@router.put("/products/{product_id}")
async def update_product(product_id: str, product_update: ProductUpdate, db: Session = Depends(get_db)) -> Any:
    product_service = ProductService(db=db)
    
    logger.info("Endpoints: update_product called.")
    msg, product_response = await product_service.update_product(product_id, product_update)
    logger.info("Endpoints: update_product called successfully.")
    return make_response_object(product_response, msg)

@router.delete("/products/{product_id}")
async def delete_product(product_id: str, db: Session = Depends(get_db)) -> Any:
    product_service = ProductService(db=db)
    
    logger.info("Endpoints: delete_product called.")
    msg, product_response = await product_service.delete_product(product_id)
    logger.info("Endpoints: delete_product called successfully.")
    return make_response_object(product_response, msg)


