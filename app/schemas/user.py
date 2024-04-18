# from datetime import datetime, date
# from typing import Optional
# from pydantic import BaseModel, constr, Field


# class UserBase(BaseModel):
#     id: Optional[str] = None
#     username: str
#     email: str
#     full_name: Optional[str] = None
#     birthday: Optional[date] = None
#     phone: Optional[str] = None


# class UserCreateParams(BaseModel):
#     email: str
#     username: str


# class UserCreateAccountParams(BaseModel):
#     username: str
#     password: str
#     password_confirm: str


# class UserCreate(BaseModel):
#     id: str
#     email: str
#     username: str


# class UserUpdate(UserBase):
#     pass


# class UserResponse(UserBase):
#     class Config:
#         orm_mode = True
#         json_encoders = {
#             datetime: lambda v: int(v.timestamp())
#         }


# class ChangePassword(BaseModel):
#     old_password: constr(min_length=6)
#     new_password: constr(min_length=6)
#     new_password_confirm: constr(min_length=6)


# class LoginUserSchema(BaseModel):
#     username: str
#     password: constr(min_length=6)


# class UserInfo(BaseModel):
#     id: str = Field(alias="user_id")
#     username: str
#     profile_image: Optional[str] = None

#     class Config:
#         allow_population_by_field_name = True
#         orm_mode = True
