from sqlalchemy import Column, ForeignKey, String
from .base import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

class PromotionBelongToBranch(Base):
    __tablename__ = "promotion_belong_to_branch"
    
    id = Column(String, primary_key=True)
    # promotion_id = Column(String,  unique = False, nullable = False)
    # branch_id = Column(String,  unique = False, nullable = False)
    
    promotion_id = Column(String, ForeignKey('promotion.id'), unique = False, nullable = False)
    branch_id = Column(String, ForeignKey('branch.id'), unique = False, nullable = False)
    
    branch = relationship('Branch')
    promotion = relationship('Promotion')