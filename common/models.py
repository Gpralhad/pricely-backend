import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, UniqueConstraint
from .database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Shop(Base):
    __tablename__ = "shops"
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    latitude = Column(Float)
    longitude = Column(Float)
    mobile_number = Column(String)
    rating = Column(Float, default=0)
    
    products = relationship("Inventory", back_populates="shop")

class Inventory(Base):
    __tablename__ = "inventory"
    id = Column(Integer, primary_key=True, autoincrement=True)
    shop_barcode = Column(String, index=True, nullable=False)
    name = Column(String, index=True, nullable=False)
    price = Column(Float, nullable=False)
    mrp = Column(Float)
    unit = Column(String)
    category = Column(String, index=True)
    sub_category = Column(String)
    shop_id = Column(String, ForeignKey("shops.id", ondelete="CASCADE"))
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    shop = relationship("Shop", back_populates="products")
    
    # Matches the SQL Unique Constraint
    __table_args__ = (UniqueConstraint('shop_id', 'shop_barcode', name='unique_barcode_per_shop'),)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    shop_id = Column(String, ForeignKey("shops.id"))
    is_active = Column(Boolean, default=True)

class PriceUpdateLog(Base):
    __tablename__ = "price_updates_log"
    id = Column(Integer, primary_key=True, autoincrement=True)
    shop_id = Column(String, ForeignKey("shops.id"))
    item_id = Column(Integer, ForeignKey("inventory.id"))
    old_price = Column(Float)
    new_price = Column(Float)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

