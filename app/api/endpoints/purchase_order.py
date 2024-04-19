import logging

from typing import Any, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session, joinedload
from pydantic import UUID4
from datetime import date

from app.api.depends import oauth2
# from app.api.depends.oauth2 import create_access_token, create_refresh_token, verify_refresh_token
from app.constant.app_status import AppStatus
from app.core.exceptions import error_exception_handler
from app.db.database import get_db
from app.models import PurchaseOrder
from app.models.employee import Employee
from app.models.order_detail import OrderDetail
# from app.schemas import ChangePassword, PurchaseOrderResponse
from app.schemas.purchase_order import PurchaseOrderCreate, PurchaseOrderCreateParams, PurchaseOrderUpdate
from app.services.purchase_order import PurchaseOrderService
from app.utils.response import make_response_object
from typing import Annotated
logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/purchase_order", summary="Tạo đơn đặt hàng")
async def create_purchase_order(
    paid : bool,
    purchase_order_create: PurchaseOrderCreateParams, 
    user: Employee = Depends(oauth2.get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    current_user = await user
    purchase_order_service = PurchaseOrderService(db=db)
    logger.info("Endpoints: create_purchase_order called.")
    
    msg, purchase_order_response = await purchase_order_service.create_purchase_order(purchase_order_create,paid,current_user.id,current_user.tenant_id)
    logger.info("Endpoints: create_purchase_order called successfully.")
    return make_response_object(purchase_order_response, msg)

@router.put("/purchase_order/update_status", summary="Cập nhật trạng thái đơn đặt hàng")
async def create_purchase_order(
 
    purchase_order_create: str, 
    user:str = None,
    db: Session = Depends(get_db)
) -> Any:
    purchase_order_service = PurchaseOrderService(db=db)
    logger.info("Endpoints: create_purchase_order called.")
    
    msg, purchase_order_response = await purchase_order_service.create_purchase_order(purchase_order_create,user)
    logger.info("Endpoints: create_purchase_order called successfully.")
    return make_response_object(purchase_order_response, msg)
@router.get("/purchase_order", summary="Lấy thông tin tất cả đơn đặt hàng")
async def get_all_purchase_order(
    db: Session = Depends(get_db),
    limit: int = None,
    offset: int = None,
    status:Optional[str] = None,
    gt_total:Optional[int] = None,
    lt_total:Optional[int] = None,
    start_date:Optional[date] = None,
    end_date:Optional[date] = None,
    query_search:Optional[str] = None
    ) -> Any:
    purchase_order_service = PurchaseOrderService(db=db)
    logger.info("Endpoints: get_all_purchase_order called.")
    
    msg, purchase_order_response = await purchase_order_service.get_all_purchase_orders(
        limit,
        offset,
        status,
        gt_total,
        lt_total,
        start_date,
        end_date,
        query_search
    )
    logger.info("Endpoints: get_all_purchase_order called successfully.")
    return make_response_object(purchase_order_response, msg)

@router.get("/purchase_order/{purchase_order_id}", summary="Lấy thông tin đơn đặt hàng theo ID đơn đặt hàng")
async def get_purchase_order_by_id(purchase_order_id: str, db: Session = Depends(get_db)) -> Any:
    purchase_order_service = PurchaseOrderService(db=db)
    
    logger.info("Endpoints: get_purchase_order_by_id called.")  
    msg, purchase_order_response = await purchase_order_service.get_purchase_order_by_id(purchase_order_id)
    logger.info("Endpoints: get_all_purchase_order called successfully.")
    return make_response_object(purchase_order_response, msg)
    
@router.put("/purchase_order/{purchase_order_id}", summary="Cập nhật thông tin đơn đặt hàng theo ID đơn đặt hàng")
async def update_purchase_order(purchase_order_id: str, purchase_order_update: PurchaseOrderUpdate, db: Session = Depends(get_db)) -> Any:
    purchase_order_service = PurchaseOrderService(db=db)
    
    logger.info("Endpoints: update_purchase_order called.")
    msg, purchase_order_response = await purchase_order_service.update_purchase_order(purchase_order_id, purchase_order_update)
    logger.info("Endpoints: update_purchase_order called successfully.")
    return make_response_object(purchase_order_response, msg)

@router.delete("/purchase_order/{purchase_order_id}",summary="Xóa thông tin đơn đặt hàng theo ID đơn đặt hàng")
async def delete_purchase_order(purchase_order_id: str, db: Session = Depends(get_db)) -> Any:
    purchase_order_service = PurchaseOrderService(db=db)
    
    logger.info("Endpoints: delete_purchase_order called.")
    msg, purchase_order_response = await purchase_order_service.delete_purchase_order(purchase_order_id)
    logger.info("Endpoints: delete_purchase_order called successfully.")
    return make_response_object(purchase_order_response, msg)