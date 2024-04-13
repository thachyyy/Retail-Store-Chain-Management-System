from sqlalchemy import Column, Integer,  Date, ForeignKey, String, DateTime
from sqlalchemy.sql import text
from .base import Base
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy

class OrderDetail(Base):
    __tablename__ = 'order'
    id = Column(Integer, primary_key= True,autoincrement= True)
    batch_id = Column(ForeignKey('batch.id'))
    purchase_order_id = Column(ForeignKey('purchase_order.id'))
    quantity = Column(Integer,nullable= False)
    price = Column(Integer,nullable =True)
    sub_total = Column(Integer,nullable = True)
    batch = relationship("Batch", back_populates="purchase_order")
    purchase_order = relationship("PurchaseOrder", back_populates="batch")
    
    # proxies
    purchase_order_name = association_proxy(target_collection='purchase_order', attr='total')
    batch_name = association_proxy(target_collection='batch', attr='quantity')
