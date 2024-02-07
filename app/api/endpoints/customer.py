import logging

from typing import Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.depends import oauth2
from app.api.depends.oauth2 import create_access_token, create_refresh_token, verify_refresh_token
from app.constant.app_status import AppStatus
from app.core.exceptions import error_exception_handler
from app.db.database import get_db
from app.models import User
from app.schemas import ChangePassword, UserResponse
from app.schemas.customer import CustomerCreateParams
from app.services.user import UserService
from app.utils.response import make_response_object

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/customer/create")
async def create_customer(
    customer_create: CustomerCreateParams,
    db: Session = Depends(get_db)
) -> Any:
    pass