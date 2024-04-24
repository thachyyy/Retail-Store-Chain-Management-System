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

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/report")
async def gen_pdf(
    name: str,
    user: Employee = Depends(oauth2.get_current_user),
    db: Session = Depends(get_db)
):
    current_user = await user
    
    print("day ne", current_user.role)
    
    if current_user.role == "Nhân viên":
        raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_ACCESS_DENIED)
    
    report_service = ReportService(db=db)
    
    res = await report_service.gen_pdf(name=name)
    
    return res
