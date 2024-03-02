from sqlalchemy import Column, String, ForeignKey
from .base import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

class PromotionForCategories(Base):
    __tablename__ = "promotion_for_categories"
    
    promotion_code = Column(String(20), ForeignKey('promotion.promotion_code'), primary_key=True)
    categories_name = Column(String(255), ForeignKey('categories.name'), primary_key=True)