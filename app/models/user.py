from sqlalchemy import Boolean, Column, String
from .base import Base


class User(Base):
    __tablename__ = "user"

    id = Column(String(255), primary_key=True)
    username = Column(String(42), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    profile_image = Column(String(255), nullable=False)
    hashed_password = Column(String)
    first_name = Column(String(255))
    last_name = Column(String(255))
    verify_code = Column(String(255))
    phone = Column(String(255))
    authenticated_google_id = Column(String(255))
    authenticated_apple = Column(String(255))
    is_register = Column(Boolean, nullable=False, default=False)
