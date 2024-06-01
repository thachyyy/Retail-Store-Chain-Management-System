import logging

from typing import Optional
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.schemas.noti import NotiCreate, NotiUpdate
from app.crud.base import CRUDBase
from ..models import Noti



logger = logging.getLogger(__name__)

class CRUDNoti(CRUDBase[Noti, NotiCreate, NotiUpdate]):
    @staticmethod
    def get_all_noties(db: Session, tenant_id: str, branch: str = None, offset: int = None, limit: int = None):
        logger.info("CRUDNoti: get_all_noties called.")
        if branch:
            query_set = db.query(Noti).filter(Noti.tenant_id == tenant_id, Noti.branch == branch, Noti.status == 0)
        else:  
            query_set = db.query(Noti).filter(Noti.tenant_id == tenant_id, Noti.status == 0)
        count = query_set.count()

        if offset is not None and limit is not None:
            query_set = query_set.offset(offset).limit(limit)

        logger.info("CRUDNoti: get_all_noties called successfully.")
        return query_set.all(), count
        
    @staticmethod
    def get_expiring_batches(db: Session):
        logger.info("CRUDNoti: get_expiring_batches is called.")
        near_expiry_date = datetime.now() + timedelta(days=7)
        sql = f"SELECT * FROM public.batch WHERE expiry_date is not null AND expiry_date <= '{near_expiry_date}' AND quantity > 0 AND status = 0;"
        result = db.execute(sql)
        result_as_dict = result.mappings().all()
        logger.info("CRUDNoti: get_expiring_batches is called successfully.")
        return result_as_dict
    
    @staticmethod
    def isExist(db: Session, batch_id: str):
        logger.info("CRUDNoti: isExist is called.")
        sql = f"SELECT * FROM public.noti WHERE batch_id = '{batch_id}';"
        result = db.execute(sql)
        result_as_dict = result.mappings().all()
        logger.info("CRUDNoti: isExist is called successfully.")
        return result_as_dict
        
    @staticmethod
    def createNoti(db: Session, obj_in: NotiCreate):
        logger.info("CRUDNoti: create called.")
        db_obj = Noti(**obj_in.dict())
        db.add(db_obj)
        db.flush()
        db.refresh(db_obj)
        logger.info("CRUDNoti: create called successfully.")
        return db_obj
    
    @staticmethod
    def updateNoti(db: Session, tenant_id: str, batch_id: str, obj_update: NotiUpdate):
        logger.info("CRUDNoti: updateNoti is called.")
        update_data = obj_update.dict(exclude_unset=True)
        result = db.query(Noti).filter(Noti.batch_id == batch_id, Noti.tenant_id == tenant_id).update(update_data)
        logger.info("CRUDNoti: updateNoti is called successfully.")
        return result
    
    @staticmethod
    def updateNotiContract(db: Session, tenant_id: str, contract_id: str, obj_update: NotiUpdate):
        logger.info("CRUDNoti: updateNoti is called.")
        update_data = obj_update.dict(exclude_unset=True)
        result = db.query(Noti).filter(Noti.contract_id == contract_id, Noti.tenant_id == tenant_id).update(update_data)
        logger.info("CRUDNoti: updateNoti is called successfully.")
        return result
    
    @staticmethod
    def update_status(db: Session, id: str, tenant_id: str, status: int):
        return db.query(Noti).update().values(status=status).where(Noti.id == id, Noti.tenant_id == tenant_id)
    
    @staticmethod
    def update_status_in_batch(db: Session, tenant_id: str, batch_id: str):
        sql = f"UPDATE public.batch SET status = 1 WHERE tenant_id = '{tenant_id}' AND id = '{batch_id}';"
        result = db.execute(sql)
        return result
    
    @staticmethod
    def get_product_name(db: Session, product_id: str):
        sql = f"SELECT product_name FROM public.product WHERE id = '{product_id}';"
        result = db.execute(sql).fetchone()
        return result[0]
    
    @staticmethod
    def get_tenant_and_branch(db: Session, product_id: str):
        sql = f"SELECT tenant_id, branch FROM public.product WHERE id = '{product_id}';"
        result = db.execute(sql).fetchone()
        return result[0], result[1]
    
    @staticmethod
    def get_list_batch_id(db: Session):
        sql = "SELECT batch_id FROM public.noti;"
        result = db.execute(sql).fetchall()
        batch_ids = [item[0] for item in result]
        return batch_ids
    
    @staticmethod
    def get_quantity_of_batch(db: Session, batch_id: str):
        sql = f"SELECT quantity, tenant_id from public.batch WHERE id = '{batch_id}';"
        result = db.execute(sql).fetchone()
        return result[0], result[1]
    
    @staticmethod
    def get_expiring_import_contract(db: Session):
        logger.info("CRUDNoti: get_expiring_import_contract is called.")
        near_expiry_date = datetime.now() + timedelta(days=10)
        sql = f"SELECT * FROM public.contract_for_vendor WHERE next_import is not null AND next_import <= '{near_expiry_date}';"
        result = db.execute(sql)
        result_as_dict = result.mappings().all()
        logger.info("CRUDNoti: get_expiring_import_contract is called successfully.")
        return result_as_dict
    
    @staticmethod
    def isExistContract(db: Session, contract_id: str):
        logger.info("CRUDNoti: isExist is called.")
        sql = f"SELECT * FROM public.noti WHERE contract_id = '{contract_id}';"
        result = db.execute(sql)
        result_as_dict = result.mappings().all()
        logger.info("CRUDNoti: isExist is called successfully.")
        return result_as_dict

    @staticmethod
    def get_tenant_and_branch_of_contract(db: Session, contract_id: str):
        sql = f"SELECT tenant_id, branch FROM public.contract_for_vendor WHERE id = '{contract_id}';"
        result = db.execute(sql).fetchone()
        return result[0], result[1]
    
noti = CRUDNoti(Noti)