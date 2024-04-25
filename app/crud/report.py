import logging
from fastapi import HTTPException
from typing import Optional
from sqlalchemy.orm import Session
from app.constant.app_status import AppStatus
from app.core.exceptions import error_exception_handler

from app.schemas.report import ReportCreate, ReportUpdate
from app.crud.base import CRUDBase
# from ..models import Report

logger = logging.getLogger(__name__)

class CRUDReport():
    @staticmethod
    async def report_inventory_quantity(db: Session, tenant_id: str, branch: str = None):
        try:
            logger.info("CRUDReport: report_inventory_quantity is called.")
            sql = f"""
                SELECT b.product_id, p.product_name , SUM(b.quantity) AS total_quantity
                FROM public.batch b 
                JOIN product p ON p.id = b.product_id 
                where b.tenant_id = '{tenant_id}' and b.branch = '{branch}'
                GROUP BY b.product_id, p.product_name ;
            """

            results = db.execute(sql)
            result_list = [dict(row) for row in results]
            logger.info("CRUDReport: report_inventory_quantity is called successfully.")
            return result_list
        except Exception as e:
            print("Execption in report_inventory_quantity:", e)
            
    @staticmethod
    async def get_user_name(db: Session, user_id: str):
        sql = f"SELECT full_name FROM public.employee WHERE id = '{user_id}';"
        result = db.execute(sql).fetchone()
        return result[0]
    
    
report = CRUDReport()