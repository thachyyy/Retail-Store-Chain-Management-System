from sqlalchemy import Column, Float, ForeignKey, String, DateTime
from .base import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

class InvoiceForCustomer(Base):
    __tablename__ = "invoice_for_customer"
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    created_at = Column(DateTime, unique = False, nullable = False)
    total = Column(Float, unique = False, nullable = False)
    status = Column(String, unique = False, nullable = False)
    payment_method = Column(String, unique = False, nullable = False)
    # belong_to_order = Column(UUID(as_uuid=True),  unique = True, nullable = False)

    belong_to_order = Column(UUID(as_uuid=True), ForeignKey('purchase_order.id'), unique = True, nullable = False)
    
    purchase_order = relationship('PurchaseOrder')