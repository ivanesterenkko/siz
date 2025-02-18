from datetime import datetime
import uuid
from sqlalchemy import UUID, Boolean, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


class Warehouses(Base):
    __tablename__ = 'warehouse'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    address: Mapped[str] = mapped_column(String, nullable=False)

    warehouse_products = relationship("Warehouses_products", back_populates="warehouse", cascade="all, delete-orphan")


class Warehouses_products(Base):
    __tablename__ = 'warehouse_product'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    update_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    product_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('product.id', ondelete='CASCADE'), nullable=False)
    warehouse_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('warehouse.id', ondelete='CASCADE'), nullable=False)

    product = relationship("Products", back_populates="warehouse_products")
    warehouse = relationship("Warehouses", back_populates="warehouse_products")
    carts = relationship("Carts", back_populates="warehouse_product", cascade="all, delete-orphan")
    order_products = relationship("Order_products", back_populates="warehouse_product", cascade="all, delete-orphan")


class Products(Base):
    __tablename__ = 'product'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    weight: Mapped[float] = mapped_column(Float, nullable=False)
    length: Mapped[float] = mapped_column(Float, nullable=False)
    width: Mapped[float] = mapped_column(Float, nullable=False)
    height: Mapped[float] = mapped_column(Float, nullable=False)
    color: Mapped[str] = mapped_column(String, nullable=False)
    country: Mapped[str] = mapped_column(String, nullable=False)
    brand: Mapped[str] = mapped_column(String, nullable=False)
    gost: Mapped[str] = mapped_column(String, nullable=False)
    article: Mapped[str] = mapped_column(String, nullable=False)
    is_by_order: Mapped[bool] = mapped_column(Boolean, nullable=False)
    produce_time: Mapped[float] = mapped_column(Float, nullable=False)
    lifespan: Mapped[float] = mapped_column(Float, nullable=False)

    supplier_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('supplier.id', ondelete='CASCADE'), nullable=False)
    category_id:  Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('category.id', ondelete='CASCADE'), nullable=False)

    supplier = relationship("Suppliers", back_populates="products")
    category = relationship("Categories", back_populates="products")
    warehouse_products = relationship("Warehouses_products", back_populates="product", cascade="all, delete-orphan")
    product_attributes = relationship("Product_attributes", back_populates="product", cascade="all, delete-orphan")


class Categories(Base):
    __tablename__ = 'category'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    class_name: Mapped[str] = mapped_column(String, nullable=False)
    product_type: Mapped[str] = mapped_column(String, nullable=False)

    products = relationship("Products", back_populates="category", cascade="all, delete-orphan")
    attributes = relationship("Attributes", back_populates="category", cascade="all, delete-orphan")


class Attributes(Base):
    __tablename__ = 'attribute'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    value_name: Mapped[str] = mapped_column(String, nullable=False)
    value_type: Mapped[str] = mapped_column(String, nullable=False)

    category_id:  Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('category.id', ondelete='CASCADE'), nullable=False)

    category = relationship("Categories", back_populates="attributes")
    product_attributes = relationship("Product_attributes", back_populates="attribute", cascade="all, delete-orphan")


class Product_attributes(Base):
    __tablename__ = 'product_attribute'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    value: Mapped[str] = mapped_column(String, nullable=False)

    product_id:  Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('product.id', ondelete='CASCADE'), nullable=False)
    attribute_id:  Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('attribute.id', ondelete='CASCADE'), nullable=False)

    product = relationship("Products", back_populates="product_attributes")
    attribute = relationship("Attributes", back_populates="product_attributes")


class Carts(Base):

    __tablename__ = 'cart'

    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)

    customer_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('customer.id', ondelete='CASCADE'), nullable=False)
    warehouse_product_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('warehouse_product.id', ondelete='CASCADE'), nullable=False)

    customer = relationship("Customers", back_populates="carts")
    warehouse_product = relationship("Warehouses_products", back_populates="carts")


class Orders(Base):

    __tablename__ = 'order'

    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    total_price: Mapped[int] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False)

    customer_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('customer.id', ondelete='CASCADE'), nullable=False)

    customer = relationship("Customers", back_populates="orders")
    order_products = relationship("Order_products", back_populates="order", cascade="all, delete-orphan")


class Order_products(Base):

    __tablename__ = 'order_product'

    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)

    order_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('order.id', ondelete='CASCADE'), nullable=False)
    warehouse_product_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('warehouse_product.id', ondelete='CASCADE'), nullable=False)

    order = relationship("Orders", back_populates="order_products")
    warehouse_product = relationship("Warehouses_products", back_populates="order_products")


class Tariffs(Base):
    __tablename__ = 'tariff'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    limit_users: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
