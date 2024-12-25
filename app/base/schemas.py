from datetime import datetime
from pydantic import UUID4, BaseModel


class ProductRequest(BaseModel):
    name: str
    description: str
    weight: float
    width: float
    length: float
    height: float
    price: int


class ProductResponse(BaseModel):
    id: UUID4
    supplier_id: UUID4
    name: str
    description: str
    weight: float
    width: float
    length: float
    height: float
    price: int


class WarehouseRequest(BaseModel):
    name: str
    address: str


class WarehouseResponse(BaseModel):
    id: UUID4
    name: str
    address: str


class Warehouse_productResponse(BaseModel):
    id: UUID4
    quantity: int
    warehouse_id: UUID4
    product_id: UUID4
    update_date: datetime


class CartsResponse(BaseModel):
    id: UUID4
    customer_id: UUID4
    warehouse_product_id: UUID4
    quantity: int


class Order_productsResponse(BaseModel):
    id: UUID4
    order_id: UUID4
    warehouse_product_id: UUID4
    quantity: int


class OrdersResponse(BaseModel):
    id: UUID4
    total_price: int
    products: list[Order_productsResponse]
    status: str
    created_at: datetime
    updated_at: datetime


class TariffRequest(BaseModel):
    name: str
    limit_users: int
    price: int


class TariffResponse(BaseModel):
    id: UUID4
    name: str
    limit_users: int
    price: int
