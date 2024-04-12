import logging

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Any, Optional

from app.db.database import get_db
from app.services.order_detail import OrderDetailService
from app.utils.response import make_response_object
# from app.schemas.order_detail import OrderDetailCreateParams, OrderDetailUpdate



logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/order_detail")
async def get_all_order_detail(
    db: Session = Depends(get_db),
    limit: Optional[int] = None,
    offset:Optional[int] = None,
) -> Any:
    order_detail_service = OrderDetailService(db=db)
    logger.info("Endpoints: get_all_order_detail called.")
    
    msg, order_detail_response = await order_detail_service.get_all_order_details(limit=limit, offset=offset)
    logger.info("Endpoints: get_all_order_detail called successfully.")
    return make_response_object(order_detail_response, msg)

@router.get("/order_detail/{order_detail_id}")
async def get_order_detail_by_id(order_detail_id: str, db: Session = Depends(get_db)) -> Any:
    order_detail_service = OrderDetailService(db=db)
    
    logger.info("Endpoints: get_order_detail_by_id called.")  
    msg, order_detail_response = await order_detail_service.get_order_detail_by_id(order_detail_id)
    logger.info("Endpoints: get_order_detail_by_id called successfully.")
    return make_response_object(order_detail_response, msg)

# @router.put("/order_detail/{order_detail_id}")
# async def update_order_detail(order_detail_id: str, order_detail_update: OrderDetailUpdate, db: Session = Depends(get_db)) -> Any:
#     order_detail_service = OrderDetailService(db=db)
    
#     logger.info("Endpoints: update_order_detail called.")
#     msg, order_detail_response = await order_detail_service.update_order_detail(order_detail_id, order_detail_update)
#     logger.info("Endpoints: update_order_detail called successfully.")
#     return make_response_object(order_detail_response, msg)

# @router.delete("/order_detail/{order_detail_id}")
# async def delete_order_detail(order_detail_id: str, db: Session = Depends(get_db)) -> Any:
#     order_detail_service = OrderDetailService(db=db)
    
#     logger.info("Endpoints: delete_order_detail called.")
#     msg, order_detail_response = await order_detail_service.delete_order_detail(order_detail_id)
#     logger.info("Endpoints: delete_order_detail called successfully.")
#     return make_response_object(order_detail_response, msg)
