import logging

from typing import Optional
from pydantic import EmailStr, UUID4

from sqlalchemy.orm import Session
from app.models.order_detail import OrderDetail
from app.schemas.order_detail import OrderDetailCreate, OrderDetailUpdate

from app.crud.base import CRUDBase
from ..models import OrderDetail

logger = logging.getLogger(__name__)


class CRUDOrderDetail(CRUDBase[OrderDetail, OrderDetailCreate, OrderDetailUpdate]):     
    
    @staticmethod
    async def get_all_order_details(db: Session) -> Optional[OrderDetail]:
        return db.query(OrderDetail).all()
    
    
    @staticmethod
    async def delete_order_detail(db: Session, order_detail_id: str):
        return db.query(OrderDetail).filter(OrderDetail.id == order_detail_id).delete()
    
    @staticmethod
    async def search_order_detail(db: Session, sql: str):        
        result = db.execute(sql)
        result_as_dict = result.mappings().all()
        return result_as_dict
    
    @staticmethod
    async def filter_order_detail(db: Session, sql: str):
        result = db.execute(sql)
        result_as_dict = result.mappings().all()
        return result_as_dict

order_detail = CRUDOrderDetail(OrderDetail)