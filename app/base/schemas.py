from datetime import datetime
from pydantic import UUID4, BaseModel


class RolesRequest(BaseModel):
    name: str
    description: str


class RolesResponse(BaseModel):
    id: UUID4
    name: str
    description: str


class Role_classesRequest(BaseModel):
    class_id: UUID4
    name: str
    lifespan: int


class Role_classesResponse(BaseModel):
    id: UUID4
    class_id: UUID4
    name: str
    lifespan: int


class Product_attributeRequest(BaseModel):
    attribute_id: UUID4
    value: str


class Product_attributeResponse(BaseModel):
    id: UUID4
    attribute_id: UUID4
    name: str
    value: str


class ProductRequest(BaseModel):
    name: str
    description: str
    weight: float
    width: float
    length: float
    height: float
    price: int
    color: str
    country: str
    brand: str
    gost: str
    article: str
    produce_time: float
    lifespan: float
    is_by_order: bool
    category_id: UUID4
    attributes: list[Product_attributeRequest]


class CategoryResponse(BaseModel):
    id: UUID4
    name: str
    class_name: str
    class_type: str


class ProductResponse(BaseModel):
    id: UUID4
    supplier_id: UUID4
    classes: CategoryResponse
    name: str
    description: str
    weight: float
    width: float
    length: float
    height: float
    price: int
    color: str
    country: str
    brand: str
    gost: str
    article: str
    produce_time: float
    lifespan: float
    is_by_order: bool
    attributes: list[Product_attributeResponse]


class WarehouseRequest(BaseModel):
    name: str
    phone: str
    representativeName: str
    address: str


class WarehouseResponse(BaseModel):
    id: UUID4
    name: str
    phone: str
    representativeName: str
    address: str


class Warehouse_productResponse(BaseModel):
    id: UUID4
    quantity: int
    warehouse_id: UUID4
    product_id: UUID4
    update_date: datetime


class CategoryRequest(BaseModel):
    name: str
    class_name: str
    class_type: str


class AttributesRequest(BaseModel):
    name: str
    value_name: str
    value_type: str


class AttributesResponse(BaseModel):
    id: UUID4
    name: str
    value_name: str
    value_type: str


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
