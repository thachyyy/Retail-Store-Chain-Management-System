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
from app.models import PurchaseOrder
from app.models.order_detail import OrderDetail
from app.schemas import ChangePassword, PurchaseOrderResponse
from app.schemas.purchase_order import PurchaseOrderCreate, PurchaseOrderCreateParams, PurchaseOrderUpdate
from app.services.purchase_order import PurchaseOrderService
from app.utils.response import make_response_object
from typing import Annotated
logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/purchase_order")
async def create_purchase_order(
    purchase_order_create: PurchaseOrderCreateParams, 
    user:str = None,
    db: Session = Depends(get_db)
) -> Any:
    purchase_order_service = PurchaseOrderService(db=db)
    logger.info("Endpoints: create_purchase_order called.")
    
    msg, purchase_order_response = await purchase_order_service.create_purchase_order(purchase_order_create,user)
    logger.info("Endpoints: create_purchase_order called successfully.")
    return make_response_object(purchase_order_response)
@router.get("/batchs_and_purchase_order/",response_model_exclude={'role'}, response_model_by_alias=False)
async def get_batch_purchase_order( 
    db: Session = Depends(get_db),
    limit: int = None,
    offset: int = None
    ):
    purchase_order_service = PurchaseOrderService(db=db)
    msg, purchase_order_response = await purchase_order_service.get_all_purchase_orders_details(limit,offset)
    db_batch_purchase_order = db.query(OrderDetail).options(joinedload(OrderDetail.purchase_order),joinedload(OrderDetail.batch)).all()
        
    return db_batch_purchase_order
@router.get("/purchase_order")
async def get_all_purchase_order(
    db: Session = Depends(get_db),
    limit: int = None,
    offset: int = None,
    # note: str = None,
    # status: str = None,
    # query_search: Optional[str] = None
    ) -> Any:
    purchase_order_service = PurchaseOrderService(db=db)
    logger.info("Endpoints: get_all_purchase_order called.")
    
    msg, purchase_order_response = await purchase_order_service.get_all_purchase_orders(limit,offset)
    logger.info("Endpoints: get_all_purchase_order called successfully.")
    return make_response_object(purchase_order_response, msg)

@router.get("/purchase_order/{purchase_order_id}")
async def get_purchase_order_by_id(purchase_order_id: str, db: Session = Depends(get_db)) -> Any:
    purchase_order_service = PurchaseOrderService(db=db)
    
    logger.info("Endpoints: get_purchase_order_by_id called.")  
    msg, purchase_order_response = await purchase_order_service.get_purchase_order_by_id(purchase_order_id)
    logger.info("Endpoints: get_all_purchase_order called successfully.")
    return make_response_object(purchase_order_response, msg)
    
@router.put("/purchase_order/{purchase_order_id}")
async def update_purchase_order(purchase_order_id: str, purchase_order_update: PurchaseOrderUpdate, db: Session = Depends(get_db)) -> Any:
    purchase_order_service = PurchaseOrderService(db=db)
    
    logger.info("Endpoints: update_purchase_order called.")
    msg, purchase_order_response = await purchase_order_service.update_purchase_order(purchase_order_id, purchase_order_update)
    logger.info("Endpoints: update_purchase_order called successfully.")
    return make_response_object(purchase_order_response, msg)

@router.delete("/purchase_order/{purchase_order_id}")
async def delete_purchase_order(purchase_order_id: str, db: Session = Depends(get_db)) -> Any:
    purchase_order_service = PurchaseOrderService(db=db)
    
    logger.info("Endpoints: delete_purchase_order called.")
    msg, purchase_order_response = await purchase_order_service.delete_purchase_order(purchase_order_id)
    logger.info("Endpoints: delete_purchase_order called successfully.")
    return make_response_object(purchase_order_response, msg)