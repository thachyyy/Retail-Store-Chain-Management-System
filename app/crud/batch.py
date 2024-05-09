import logging

from pydantic import EmailStr
from typing import Optional
from sqlalchemy.orm import Session

from app.schemas.batch import BatchCreate, BatchUpdate
from app.crud.base import CRUDBase
from ..models import Batch

from app.core.exceptions import error_exception_handler
from app.constant.app_status import AppStatus

logger = logging.getLogger(__name__)

class CRUDBatch(CRUDBase[Batch, BatchCreate, BatchUpdate]):
    @staticmethod
    async def get_all_batches(db: Session) -> Optional[Batch]:
        return db.query(Batch).all()

    @staticmethod
    async def get_batch_by_id(db: Session, batch_id: str, tenant_id: str):
        return db.query(Batch).filter(Batch.id == batch_id, Batch.tenant_id == tenant_id).first()
    
    @staticmethod
    async def get_batch_by_product_id(db: Session, product_id: str, tenant_id: str):
        sql = f"""SELECT batch.id AS batch_id, batch.created_at AS batch_created_at, batch.updated_at AS batch_updated_at, 
                         batch.quantity AS batch_quantity, batch.import_price AS batch_import_price, 
                         batch.manufacturing_date AS batch_manufacturing_date, batch.expiry_date AS batch_expiry_date, 
                         batch.branch AS batch_branch, batch.product_id AS batch_product_id, batch.belong_to_receipt AS batch_belong_to_receipt, 
                         batch.tenant_id AS batch_tenant_id, batch.status AS batch_status 
                  FROM batch
                  WHERE batch.product_id = '{product_id}' AND batch.tenant_id = '{tenant_id}';
        """
        result = db.execute(sql).fetchall()
        list_result = [item for item in result]
        
        sql_sum = f"""SELECT sum(batch.quantity) as sum_quantity
                      FROM batch
                      WHERE batch.product_id = '{product_id}' AND batch.tenant_id = '{tenant_id}';
        """
        sum = db.execute(sql_sum).fetchone()
        if sum[0]:
            sum = int(sum[0])  # Chuyển kết quả thành số
        else: sum = None
        
        return list_result, sum
    
    @staticmethod
    async def get_batch_by_conditions(db: Session, sql: str, total: str):        
        result = db.execute(sql)
        sum = db.execute(total)
        sum = sum.mappings().all()
        result_as_dict = result.mappings().all()
        return result_as_dict, sum 
    @staticmethod
    async def get_last_id(db: Session):
        sql = "SELECT MAX(SUBSTRING(id FROM '[0-9]+')::INT) FROM batch;"
        last_id = db.execute(sql).scalar_one_or_none()
        if last_id is None:
            return 0
        return last_id
    
    
    @staticmethod
    def create(db: Session, *, obj_in: BatchCreate) -> Batch:
        logger.info("CRUDBatch: create called.")
        logger.debug("With: BatchCreate - %s", obj_in.dict())

        db_obj = Batch(**obj_in.dict())
        db.add(db_obj)
        db.flush()
        db.refresh(db_obj)
        logger.info("CRUDBatch: create called successfully.")
        return db_obj
    
    @staticmethod
    async def update_batch(db: Session, batch_id: str, batch_update: BatchUpdate, tenant_id: str):
        update_data = batch_update.dict(exclude_unset=True)
        return db.query(Batch).filter(Batch.id == batch_id).update(update_data)
    @staticmethod
    async def update_quantity(db: Session,batch_id:str, quantity:int,tenant_id:str) -> Optional[Batch]:
        get_quantity= f"SELECT quantity FROM public.batch WHERE id = '{batch_id}' and tenant_id ='{tenant_id}' ;"
        current_quantity= db.execute(get_quantity)
        result = current_quantity.mappings().all()

        new_quantity = result[0]['quantity'] - quantity
        if new_quantity < 0: 
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_QUANITY_NOT_ENOUGH)
        sql = f"UPDATE public.batch SET quantity = {new_quantity} WHERE id = '{batch_id}';"
        result = db.execute(sql)
        return result
    @staticmethod
    async def delete_batch(db: Session, batch_id: str):
        try:
            return db.query(Batch).filter(Batch.id == batch_id).delete()
        except:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_DATA_USED_ERROR)
    
    
    
batch = CRUDBatch(Batch)