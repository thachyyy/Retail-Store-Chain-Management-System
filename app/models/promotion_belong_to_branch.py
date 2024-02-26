from sqlalchemy import Column, Float
from .base import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

class PromotionBelongToBranch(Base):
    __tablename__ = "peomotion_belong_to_branch"
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    promotion_id = Column(UUID(as_uuid=True), ForeignKey = ('promotion.id'), unique = False, nullable = False)
    branch_id = Column(UUID(as_uuid=True), ForeignKey = ('branch.id'), unique = False, nullable = False)
    
    branch = relationship('Branch')
    promotion = relationship('Promotion')