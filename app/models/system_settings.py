from sqlalchemy import (Column, String, text, Boolean)

from .base import Base


class SystemSettings(Base):
    __tablename__ = "system_settings"

    id = Column(
        String,
        primary_key=True,
        unique=True,
        server_default=text("uuid_generate_v4()"),
    )
    is_maintain = Column(Boolean, nullable=False, default=False)
