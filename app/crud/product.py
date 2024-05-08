import logging

from typing import Optional

from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from pydantic import EmailStr, UUID4

from sqlalchemy.orm import Session
from app.models.batch import Batch
from app.schemas.product import ProductCreate, ProductUpdate
from app.crud.base import CRUDBase
from ..models import Product

from app.core.exceptions import error_exception_handler
from app.constant.app_status import AppStatus

logger = logging.getLogger(__name__)


class CRUDProduct(CRUDBase[Product, ProductCreate, ProductUpdate]):    
    @staticmethod
    async def get_list_product(db: Session, tenant: str, branch: str = None):
        pass
    
    @staticmethod
    async def get_all_product(db: Session, total: str, sql: str):
        result = db.execute(sql)
        count = db.execute(total)
        
        result_as_dict = result.mappings().all()
        count = count.mappings().all()
        query = (
            db.query(func.count())
            .select_from(Product)
            .outerjoin(Batch, Product.id == Batch.product_id)
        )

        # Execute the query
        result = query.scalar()
        return result_as_dict, count
    
    
    # @staticmethod
    # async def get_products_with_pagination(limit_value:int, offset_value:int, total:str, db: Session) -> Optional[Product]:
    #     result = db.query(Product).limit(limit_value).offset(offset_value).all()
        
    #     sum = db.execute(total)
    #     sum = sum.mappings().all()
    #     return result, sum
    @staticmethod
    async def get_product_by_name(db: Session, name: str, tenant_id: str, branch: str = None) -> Optional[Product]:
        if branch is None:
            return db.query(Product).filter(Product.product_name == name, Product.tenant_id == tenant_id).first()
        return db.query(Product).filter(Product.product_name == name, Product.tenant_id == tenant_id, Product.branch == branch).first()
    
    @staticmethod
    async def check_product_exist(db: Session, id :str, tenant_id: str, branch: str = None) -> Optional[Product]:
        return db.query(Product).filter(Product.id == id,Product.tenant_id == tenant_id, Product.branch == branch).first()
    
    @staticmethod
    async def check_product_by_barcode(db: Session, barcode: str, tenant_id: str, branch: str = None) -> Optional[Product]:
        return db.query(Product).filter(Product.barcode == barcode, Product.tenant_id == tenant_id, Product.branch == branch).first()
    
    @staticmethod
    async def get_product_by_barcode(db: Session, tenant_id: str, barcode: str,branch: str = None, id: str = None) -> Optional[Product]:
        if id:
            return db.query(Product).filter(Product.barcode == barcode, Product.id != id, Product.tenant_id == tenant_id, Product.branch == branch).first()
        else:
            
            return db.query(Product).filter(Product.barcode == barcode, Product.tenant_id == tenant_id, Product.branch == branch).first()
    
    @staticmethod
    async def get_product_by_id(db: Session, tenant_id: str, product_id: str, branch: str = None):
        if branch:
            return db.query(Product).filter(Product.id == product_id, Product.tenant_id == tenant_id, Product.branch == branch).first()
        else:
            return db.query(Product).filter(Product.id == product_id, Product.tenant_id == tenant_id).first()
    
    @staticmethod
    async def get_categories_name(db: Session, categories_id: str, tenant_id: str, branch: str = None):
        sql = f"SELECT name FROM public.categories WHERE id = '{categories_id}' AND tenant_id = '{tenant_id}' AND branch = '{branch}';"
        result = db.execute(sql).fetchone()
       
        if result: 
            name = result[0]
            return name 
        else: return None
        
    
    @staticmethod
    async def get_last_id(db: Session):
        sql = "SELECT MAX(SUBSTRING(id FROM '[0-9]+')::INT) FROM product;"
        last_id = db.execute(sql).scalar_one_or_none()
        if last_id is None:
            return 0
        return last_id
    
    @staticmethod
    async def update_product(db: Session, product_id: str, product_update: ProductUpdate):
        update_data = product_update.dict(exclude_unset=True)
        return db.query(Product).filter(Product.id == product_id).update(update_data)
    
    @staticmethod
    async def delete_product(db: Session, product_id: str):
        try:
            return db.query(Product).filter(Product.id == product_id).delete()
        except:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_DATA_USED_ERROR)
    
    @staticmethod
    async def get_product_by_conditions(db: Session, sql: str, total: str):        
        result = db.execute(sql)
        sum = db.execute(total)
        sum = sum.mappings().all()
        result_as_dict = result.mappings().all()
        return result_as_dict, sum
    
    @staticmethod
    def create(db: Session, *, obj_in: ProductCreate) -> Product:
        logger.info("CRUDProduct: create called.")
        logger.debug("With: ProductCreate - %s", obj_in.dict())

        db_obj = Product(**obj_in.dict())
        db.add(db_obj)
        db.flush()
        db.refresh(db_obj)
        logger.info("CRUDProduct: create called successfully.")
        return db_obj
    
    @staticmethod
    async def insert_img_url(db: Session, tenant_id: str, url: str, product_id: str):
        try:
            if url != "":
                sql = f"UPDATE public.product SET img_url = '{url}' WHERE id = '{product_id}' AND tenant_id = '{tenant_id}';"
                db.execute(sql)
                db.commit()
                return "Success"
            else:
                ql = f"UPDATE public.product SET img_url = NULL WHERE id = '{product_id}' AND tenant_id = '{tenant_id}';"
                db.execute(sql)
                db.commit()
                return "Success"
        except Exception as e:
            print("Exception when upload img:", e)

product = CRUDProduct(Product)