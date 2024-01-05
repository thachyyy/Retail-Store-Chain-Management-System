import logging
import jwt
import requests

from fastapi import Depends, HTTPException, status, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session, sessionmaker

from app.db.database import get_db, get_session_maker
from app.models import SystemSettings
from app.core.settings import settings
from app import crud
import httpx

logger = logging.getLogger(__name__)


def validate_maintain(db: Session):
    try:
        system_settings = db.query(SystemSettings).first()
        return system_settings
    except Exception as err:
        logger.info("Service: router_middleware failed.")
        logger.error("Service: Exception.", exc_info=err)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="HTTP_500_INTERNAL_SERVER_ERROR"
        )


def router_middleware(db: Session = Depends(get_db)):
    logger.info("Service: router_middleware called.")
    system_settings = validate_maintain(db=db)
    if not system_settings or system_settings.is_maintain:
        logger.info("Service: is_maintain")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="HTTP_503_SERVICE_UNAVAILABLE"
        )
