import logging
from fastapi import HTTPException
from typing import Optional
from sqlalchemy.orm import Session
from app.constant.app_status import AppStatus
from app.core.exceptions import error_exception_handler

# from app.schemas.dashboard import DashboardCreate, DashboardUpdate
from app.crud.base import CRUDBase
from datetime import date

logger = logging.getLogger(__name__)

class CRUDDashboard():
    @staticmethod
    async def get_total_sales(db: Session, start_date: date, end_date: date, tenant_id: str, branch: str = None):
        if branch:  
            sql = f"""SELECT sum(total) 
                      FROM public.invoice_for_customer 
                      WHERE tenant_id = '{tenant_id}' 
                            AND branch = '{branch}' 
                            AND status = 'Đã thanh toán'
                            AND created_at >= '{start_date}'
                            AND created_at <= '{end_date}';
            """
        else:
            sql = f"""SELECT sum(total) 
                      FROM public.invoice_for_customer 
                      WHERE tenant_id = '{tenant_id}'
                            AND status = 'Đã thanh toán'
                            AND created_at >= '{start_date}'
                            AND created_at <= '{end_date}';
            """
        
        result = db.execute(sql).fetchone()
        return result[0]
    
    @staticmethod
    async def get_total_order(db: Session, start_date: date, end_date: date, tenant_id: str, branch: str = None):
        if branch:
            sql = f"""SELECT COUNT(*)
                      FROM public.invoice_for_customer
                      WHERE tenant_id = '{tenant_id}'
                            AND branch = '{branch}'
                            AND status = 'Đã thanh toán'
                            AND created_at >= '{start_date}'
                            AND created_at <= '{end_date}';
            """
        else:
            sql = f"""SELECT COUNT(*)
                      FROM public.invoice_for_customer
                      WHERE tenant_id = '{tenant_id}'
                            AND status = 'Đã thanh toán'
                            AND created_at >= '{start_date}'
                            AND created_at <= '{end_date}';
            """
            
        result = db.execute(sql).fetchone()
        return result[0]
    
    @staticmethod
    async def get_total_new_customer(db: Session, start_date: date, end_date: date, tenant_id: str, branch: str = None):
        sql = f"""SELECT COUNT(*)
                  FROM public.customer
                  WHERE tenant_id = '{tenant_id}'
                        AND created_at >= '{start_date}'
                        AND created_at <= '{end_date}';
            """
            
        result = db.execute(sql).fetchone()
        return result[0]
    
    @staticmethod
    async def get_import_price(db: Session, batch_id: str, tenant_id: str, branch: str = None):
        if branch:
            sql = f"""SELECT import_price
                      FROM public.batch
                      WHERE tenant_id = '{tenant_id}'
                            AND branch = '{branch}'
                            AND id = '{batch_id}';
            """
        else:
            sql = f"""SELECT import_price
                      FROM public.batch
                      WHERE tenant_id = '{tenant_id}'
                            AND id = '{batch_id}';
            """
            
        result = db.execute(sql).fetchone()
        return result[0]
    
dashboard = CRUDDashboard()