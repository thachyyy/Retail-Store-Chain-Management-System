import logging

from typing import Any, Optional
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
from app.schemas import ChangePassword, ProductResponse
from app.schemas.product import ProductCreateParams, ProductUpdate
from app.services.product import ProductService
from app.utils.response import make_response_object

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/products")
async def create_product(
    product_create: ProductCreateParams,
    db: Session = Depends(get_db)
) -> Any:
    product_service = ProductService(db=db)
    logger.info("Endpoints: create_product called.")
    
    msg, product_response = await product_service.create_product(product_create)
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
    db: Session = Depends(get_db)
) -> Any:
    product_service = ProductService(db=db)
    logger.info("Endpoints: get_all_products called.")
    msg,product_response= await product_service.get_all_products(limit,offset,status,low_price,high_price,categories)
    
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


@router.get("/product/search")
async def search_product(
    limit:int,
    offset:int,
    db: Session = Depends(get_db), 
    condition: Optional[str] = Query(None)) -> Any:
    
    product_service = ProductService(db=db)
    
    logger.info("Endpoints: search_product called.")
    msg, product_response = await product_service.search_product(limit,offset,condition)
    logger.info("Endpoints: search_product called successfully.")
    
    return make_response_object(product_response, msg)