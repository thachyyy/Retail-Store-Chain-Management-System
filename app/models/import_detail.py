from sqlalchemy import Column, Integer, String, Date, ForeignKey, DateTime
from sqlalchemy.sql import text
from .base import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


class ImportDetail(Base):
    __tablename__ = "import_detail"
    id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    product_id = Column(String,)
    product_name = Column(String)
    unit = Column(String(255),nullable=False)
    import_price = Column(Integer)
    expiry_date = Column(Date,unique=False,nullable = True)
    quantity = Column(Integer)
    sub_total = Column(Integer)
    branch = Column(String,unique =False,nullable =True)
    tenant_id = Column(String, unique=False, nullable=False)

