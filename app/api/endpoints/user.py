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
from app.schemas.user import UserUpdate, UserCreateParams, LoginUserSchema, UserCreateAccountParams
from app.services.user import UserService
from app.utils.response import make_response_object

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/users/me")
async def read_user_me(
        user: User = Depends(oauth2.get_current_active_user),
        db: Session = Depends(get_db),
) -> Any:
    """
    Get current user.
    """
    user_service = UserService(db=db)
    logger.info("Service: read_user_me called.")

    profile = await user_service.get_user_me(uid=user.id)
    logger.info("Service: read_user_me successfully.")
    return make_response_object(profile)


@router.get("/users/user_info/{username}")
async def get_user(
        username: str,
        user: User = Depends(oauth2.get_current_active_user),
        db: Session = Depends(get_db),
) -> Any:
    """
    Get current user.
    """
    user_service = UserService(db=db)
    logger.info("Service: get_user called.")

    profile = await user_service.get_user(username=username)
    user_response = [UserResponse.from_orm(profile) for profile in profile]
    logger.info("Service: get_user successfully.")
    return make_response_object(user_response)


@router.post('/auth/register')
async def create_user(
        user_create: UserCreateAccountParams,
        db: Session = Depends(get_db)
) -> Any:
    """
    Create user.
    """
    user_service = UserService(db=db)
    logger.info("Endpoints: create_user called.")

    user_response = await user_service.create_user(user_create)
    logger.info("Endpoints: create_user called successfully.")
    return make_response_object(user_response)


@router.post("/auth/login")
async def login(
        login_request: LoginUserSchema,
        db: Session = Depends(get_db),
) -> Any:
    """
    login social.
    """
    logger.info("Service: read_user_me called.")

    user_service = UserService(db=db)
    current_user = await user_service.login(login_request)

    created_access_token = create_access_token(data={"uid": current_user.id})
    created_refresh_token = create_refresh_token(data={"uid": current_user.id})
    logger.info("Service: read_user_me successfully.")
    return make_response_object(data=dict(access_token=created_access_token,
                                          refresh_token=created_refresh_token),
                                meta=AppStatus.LOGIN_SUCCESS.meta)


@router.post("/auth/refresh")
async def refresh_token(decoded_refresh_token=Depends(verify_refresh_token),
                        db: Session = Depends(get_db)):
    logger.info("Service: refresh_token called.")
    user_service = UserService(db=db)
    current_user = await user_service.get_user_by_id(decoded_refresh_token['uid'])

    if not current_user:
        raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_USER_NOT_FOUND)

    created_access_token = create_access_token(data={"uid": current_user.id})
    created_refresh_token = create_refresh_token(data={"uid": current_user.id})
    logger.info("Service: refresh_token called successfully.")
    return make_response_object(data=dict(access_token=created_access_token,
                                          refresh_token=created_refresh_token))


@router.put("/users/update_me")
async def update_profile(
        user_update: UserUpdate,
        user: User = Depends(oauth2.get_current_active_user),
        db: Session = Depends(get_db)

) -> Any:
    """
    Update Profile : Update Profile.
    """
    user_service = UserService(db=db)
    logger.info("Service: update_profile called.")

    await user_service.update_user_profile(user_id=user.id, obj_in=user_update)
    logger.info("Service: update_profile successfully.")
    return dict(message_code=AppStatus.SUCCESS.message)


@router.put("/auth/reset_password")
async def change_password(
        request: ChangePassword,
        user: User = Depends(oauth2.get_current_active_user),
        db: Session = Depends(get_db)
):
    logger.info("Endpoints: change_password called.")
    user_service = UserService(db=db)
    await user_service.change_password(username=user.username, obj_in=request)
    logger.info("Endpoints: change_password called successfully.")
    return dict(message_code=AppStatus.SUCCESS.message)


@router.put("/auth/forget_password")
async def forget_password(
        email: str,
        username: str,
        db: Session = Depends(get_db)
) -> Any:
    user_service = UserService(db=db)
    logger.info("Service: get_verification_code called.")

    user_response = await user_service.get_verification_code(email=email, username=username, action="forget_password")

    logger.info("Endpoints: get_verification_code called successfully.")
    return make_response_object(user_response)


@router.put("/auth/verify_code")
async def verify_code(
        email: str,
        username: str,
        verify_code: str,
        new_password: str,
        password_confirm: str,
        db: Session = Depends(get_db)
) -> Any:
    user_service = UserService(db=db)
    logger.info("Service: verify_code called.")

    user_response = await user_service.verify_code(email=email,
                                                   username=username,
                                                   verify_code=verify_code,
                                                   new_password=new_password,
                                                   password_confirm=password_confirm)

    logger.info("Endpoints: verify_code called successfully.")
    return make_response_object(user_response)


@router.put("/users/{user_id}/update_user")
async def update_user(
        user_id: str,
        user_update: UserUpdate,
        user: User = Depends(oauth2.get_current_active_user),
        db: Session = Depends(get_db)

) -> Any:
    user_service = UserService(db=db)
    logger.info("Service: update_profile called.")

    await user_service.update_user_profile(user_id=user_id, obj_in=user_update)
    logger.info("Service: update_profile successfully.")
    return dict(message_code=AppStatus.SUCCESS.message)


@router.delete("/users/{user_id}/")
async def delete_user(
        user_id: str,
        user: User = Depends(oauth2.get_current_active_user),
        db: Session = Depends(get_db)
):
    user_service = UserService(db=db)
    logger.info("Endpoints: delete_user called")
    user_response = await user_service.delete_user(user_id=user_id)
    logger.info("Endpoints: delete_user called successfully.")
    return make_response_object(user_response)
