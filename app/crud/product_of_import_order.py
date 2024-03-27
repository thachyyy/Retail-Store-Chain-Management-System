import logging

from pydantic import EmailStr
from typing import Optional
from sqlalchemy.orm import Session

from app.schemas.product_of_import_order import ProductOfImportOrderCreate, ProductOfImportOrderUpdate
from app.crud.base import CRUDBase
from ..models import ProductOfImportOrder

logger = logging.getLogger(__name__)

class CRUDProductOfImportOrder(CRUDBase[ProductOfImportOrder, ProductOfImportOrderCreate, ProductOfImportOrderUpdate]):
    @staticmethod
    async def get_all_product_of_import_orders(db: Session) -> Optional[ProductOfImportOrder]:
        return db.query(ProductOfImportOrder).all()
    
    @staticmethod
    async def get_product_of_import_order_by_id(db: Session, product_of_import_order_id: str):
        return db.query(ProductOfImportOrder).filter(ProductOfImportOrder.id == product_of_import_order_id).first()
    
    @staticmethod
    async def get_last_id(db: Session):
        sql = "SELECT MAX(SUBSTRING(id FROM '[0-9]+')::INT) FROM product_of_import_order;"
        last_id = db.execute(sql).scalar_one_or_none()
        if last_id is None:
            return 0
        return last_id
    
    
    @staticmethod
    def create(db: Session, *, obj_in: ProductOfImportOrderCreate) -> ProductOfImportOrder:
        logger.info("CRUDProductOfImportOrder: create called.")
        logger.debug("With: ProductOfImportOrderCreate - %s", obj_in.dict())

        db_obj = ProductOfImportOrder(**obj_in.dict())
        db.add(db_obj)
        db.flush()
        db.refresh(db_obj)
        logger.info("CRUDProductOfImportOrder: create called successfully.")
        return db_obj
    
    @staticmethod
    async def update_product_of_import_order(db: Session, product_of_import_order_id: str, product_of_import_order_update: ProductOfImportOrderUpdate):
        update_data = product_of_import_order_update.dict(exclude_unset=True)
        return db.query(ProductOfImportOrder).filter(ProductOfImportOrder.id == product_of_import_order_id).update(update_data)
    
    @staticmethod
    async def delete_product_of_import_order(db: Session, product_of_import_order_id: str):
        return db.query(ProductOfImportOrder).filter(ProductOfImportOrder.id == product_of_import_order_id).delete()
    
    
    
product_of_import_order = CRUDProductOfImportOrder(ProductOfImportOrder)