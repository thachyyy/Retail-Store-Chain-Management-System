from datetime import datetime, date
from typing import Optional
from pydantic import BaseModel, constr, Field

class UserCreateParams(BaseModel):
    email: str
    username: str