from datetime import datetime
from pydantic import UUID4, BaseModel


class RolesRequest(BaseModel):
    name: str
    description: str


class RolesResponse(BaseModel):
    id: UUID4
    name: str
    description: str


class ProductAttributesRequest(BaseModel):
    attribute_id: UUID4
    attribute_value_id: UUID4


class Role_classesRequest(BaseModel):
    class_id: UUID4
    category: str
    lifespan: int
    product_attrubutes: list[ProductAttributesRequest]


class ProductAttributesResponse(BaseModel):
    id: UUID4


class AddProductRequest(BaseModel):
    product_id: UUID4


class Role_classesResponse(BaseModel):
    id: UUID4
    product_attrubutes: list[ProductAttributesResponse]


class Product_attributeRequest(BaseModel):
    attribute_id: UUID4
    value: str


class Product_attributeResponse(BaseModel):
    id: UUID4
    attribute_id: UUID4
    name: str
    value_id: UUID4
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
    category: str
    produce_time: float
    lifespan: float
    is_by_order: bool
    class_id: UUID4


class CategoryResponse(BaseModel):
    count_products: int
    name: str
    id: UUID4


class ClassTypesResponse(BaseModel):
    count_classes: int
    type: str


class ClassesResponse(BaseModel):
    id: UUID4
    type: str
    name: str


class ProductResponse(BaseModel):
    id: UUID4
    supplier_id: UUID4
    classes: ClassesResponse
    name: str
    description: str
    category: str
    product_attrubutes: list[Product_attributeResponse]
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
    items_available: None
    pictures: None
    certificates: None
    attributes: list[Product_attributeResponse]


class AddressesRequest(BaseModel):
    region: str
    city: str
    street: str
    house: str
    building: str
    structure: str
    flat: str


class WarehouseRequest(BaseModel):
    name: str
    phone: str
    representativeName: str
    address: AddressesRequest


class WarehousePatchRequest(WarehouseRequest):
    address_id: UUID4


class AddWarehouseResponse(BaseModel):
    warehouse_id: UUID4
    datetime_created: datetime
    address_id: UUID4


class WarehouseResponse(BaseModel):
    id: UUID4
    name: str
    phone: str
    representativeName: str
    address_id: UUID4
    address: AddressesRequest


class Warehouse_productResponse(BaseModel):
    id: UUID4
    quantity: int
    warehouse_id: UUID4
    product_id: UUID4
    update_date: datetime


class CategoryRequest(BaseModel):
    name: str
    type: str


class AttributesRequest(BaseModel):
    class_id: UUID4
    name: str
    is_protection: bool


class Attribute_valuiesRequest(BaseModel):
    attribute_id: UUID4
    name: str


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
