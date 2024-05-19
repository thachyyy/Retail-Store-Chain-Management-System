import logging
from fastapi import HTTPException
from typing import Optional
from sqlalchemy.orm import Session
from app.constant.app_status import AppStatus
from app.core.exceptions import error_exception_handler

from app.schemas.report import ReportCreate, ReportUpdate
from app.crud.base import CRUDBase
from datetime import date

logger = logging.getLogger(__name__)

class CRUDReport():
    @staticmethod
    async def report_inventory_quantity(db: Session, tenant_id: str, branch: str = None):
        try:
            logger.info("CRUDReport: report_inventory_quantity is called.")
            if branch:
                sql = f"""
                    SELECT b.product_id, p.product_name , SUM(b.quantity) AS total_quantity
                    FROM public.batch b 
                    JOIN product p ON p.id = b.product_id 
                    where b.tenant_id = '{tenant_id}' and b.branch = '{branch}'
                    GROUP BY b.product_id, p.product_name ;
                """
            else:
                sql = f"""
                    SELECT b.product_id, p.product_name , SUM(b.quantity) AS total_quantity
                    FROM public.batch b 
                    JOIN product p ON p.id = b.product_id 
                    where b.tenant_id = '{tenant_id}'
                    GROUP BY b.product_id, p.product_name ;
                """

            results = db.execute(sql)
            result_list = [dict(row) for row in results]
            logger.info("CRUDReport: report_inventory_quantity is called successfully.")
            return result_list
        except Exception as e:
            print("Execption in report_inventory_quantity:", e)
            
    @staticmethod
    async def sales_report_by_branch(db: Session, tenant_id: str, start_date: date, end_date: date):
        try:
            logger.info("CRUDReport: sales_report_by_branch is called.")
            sql = f"""
            SELECT branch, COUNT(*), sum(total)
            FROM invoice_for_customer
            WHERE tenant_id = '{tenant_id}'
                AND status = 'Đã thanh toán'
                AND created_at >= '{start_date}'
                AND created_at <= '{end_date}'
            GROUP BY branch
            order by branch;
            """
            
            results = db.execute(sql)
            result_list = [dict(row) for row in results]
            logger.info("CRUDReport: sales_report_by_branch is called successfully.")
            return result_list
        except Exception as e:
            print("Execption in sales_report_by_branch:", e)
            
    @staticmethod
    async def get_price_and_name_by_product_id(db: Session, product_id: str, tenant_id: str, branch: str = None):
        if branch:
            sql = f"SELECT product_name, sale_price FROM public.product WHERE id = '{product_id}' AND tenant_id = '{tenant_id}' AND branch = '{branch}';"
        else:
            sql = f"SELECT product_name, sale_price FROM public.product WHERE id = '{product_id}' AND tenant_id = '{tenant_id}';"
            
        result = db.execute(sql).fetchone()
        return result[0], result[1]
                    
    @staticmethod
    async def get_user_name(db: Session, user_id: str):
        sql = f"SELECT full_name FROM public.employee WHERE id = '{user_id}';"
        result = db.execute(sql).fetchone()
        return result[0]
    
    @staticmethod
    async def sales_report_by_customer(db: Session, start_date: date, end_date: date, tenant_id: str, branch: str = None):
        if branch:
            sql = f"""SELECT po.belong_to_customer as customer_id, c.full_name, sum(total)
                      FROM purchase_order po
                      JOIN customer c on po.belong_to_customer = c.id
                      WHERE po.tenant_id = '{tenant_id}'
                        AND po.branch = '{branch}'
                        AND po.created_at >= '{start_date}'
                        AND po.created_at <= '{end_date}'
                        AND po.belong_to_customer is not null
                        GROUP BY po.belong_to_customer, c.id;
            """
        else:
            sql = f"""SELECT po.belong_to_customer as customer_id, c.full_name, sum(total)
                      FROM purchase_order po
                      JOIN customer c on po.belong_to_customer = c.id
                      WHERE po.tenant_id = '{tenant_id}'
                        AND po.created_at >= '{start_date}'
                        AND po.created_at <= '{end_date}'
                        AND po.belong_to_customer is not null
                        GROUP BY po.belong_to_customer, c.id;
            """

        results = db.execute(sql)
        result_list = [dict(row) for row in results]
        
        return result_list
    
    @staticmethod
    async def get_name_by_categories_id(db: Session, id: str, tenant_id: str, branch: str = None):
        if branch:
            sql = f"SELECT name FROM public.categories WHERE id = '{id}' AND tenant_id = '{tenant_id}' AND branch = '{branch}';"
        else:
            sql = f"SELECT name FROM public.categories WHERE id = '{id}' AND tenant_id = '{tenant_id}';"
            
        result = db.execute(sql).fetchone()
        if result:
            return str(result[0])  # Chuyển kết quả thành chuỗi
        return None
    
    @staticmethod
    async def get_categories_name_of_product(db: Session, id: str, tenant_id: str, branch: str = None):
        if branch:
            sql = f"""select c.name
                      from product p 
                      join categories c on p.categories_id = c.id 
                      where p.id = '{id}' and p.tenant_id = '{tenant_id}' and p.branch = '{branch}';
            """
        else:
            sql = f"""select c.name
                      from product p 
                      join categories c on p.categories_id = c.id 
                      where p.id = '{id}' and p.tenant_id = '{tenant_id}';
            """
        result = db.execute(sql).fetchone()
        if result:
            return str(result[0])  # Chuyển kết quả thành chuỗi
        return None     
    
    @staticmethod
    async def get_categories_of_product(db: Session, id: str, tenant_id: str, branch: str = None):
        if branch:
            sql = f"SELECT categories_id FROM public.product WHERE id = '{id}' AND tenant_id = '{tenant_id}' AND branch = '{branch}';"
        else:
            sql = f"SELECT categories_id FROM public.product WHERE id = '{id}' AND tenant_id = '{tenant_id}';"
            
        result = db.execute(sql).fetchone()
        if result:
            return str(result[0])  # Chuyển kết quả thành chuỗi
        return None
    
    @staticmethod
    async def get_price_of_product(db: Session, id: str, tenant_id: str, branch: str = None):
        if branch:
            sql = f"SELECT sale_price FROM public.product WHERE id = '{id}' AND tenant_id = '{tenant_id}' AND branch = '{branch}';"
        else:
            sql = f"SELECT sale_price FROM public.product WHERE id = '{id}' AND tenant_id = '{tenant_id}';"
            
        result = db.execute(sql).fetchone()
        if result:
            return int(result[0])  # Chuyển kết quả thành số
        return None
    
report = CRUDReport()