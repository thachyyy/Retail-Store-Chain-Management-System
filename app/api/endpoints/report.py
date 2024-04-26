import logging

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Any, Optional

from app.db.database import get_db
from app.api.depends import oauth2
from app.constant.app_status import AppStatus
from app.core.exceptions import error_exception_handler
from app.services.report import ReportService
from app.utils.response import make_response_object
# from app.schemas.vendor import VendorCreateParams, VendorUpdate
from app.models import Employee

from fastapi import FastAPI, Response
from fastapi.responses import StreamingResponse
import pdfkit
from starlette.responses import FileResponse
from fastapi.responses import Response
from datetime import date

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/report/inventory_quantity")
async def report_inventory_quantity(
    branch: str = None,
    user: Employee = Depends(oauth2.get_current_user),
    db: Session = Depends(get_db)
):
    current_user = await user
    
    if current_user.role == "Nhân viên":
        raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_ACCESS_DENIED)
    
    if branch:
        branch = branch
    else:
        branch= current_user.branch
        
    report_service = ReportService(db=db)
    res = await report_service.report_inventory_quantity(current_user.id, current_user.tenant_id, branch)
    
    return res

@router.get("/report/sales_by_branch")
async def sales_report_by_branch(
    start_date: date,
    end_date: date,
    user: Employee = Depends(oauth2.get_current_user),
    db: Session = Depends(get_db)
):
    current_user = await user
    if current_user.role != "Quản lý":
        raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_ACCESS_DENIED)
    
    report_service = ReportService(db=db)
    res = await report_service.sales_report_by_branch(current_user.id, start_date, end_date, current_user.tenant_id)
    
    return res