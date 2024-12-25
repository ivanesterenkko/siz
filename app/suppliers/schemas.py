from datetime import datetime
from pydantic import UUID4, BaseModel


class SupplierRegister(BaseModel):
    name: str
    INN: str
    login: str
    address: str
    phone: str
    password: str


class CompanyProjectResponse(BaseModel):
    id: UUID4
    project_name: str
    project_step: int
    user_id: UUID4
    datetime_created: datetime


class OrderRequest(BaseModel):
    tariff_id: UUID4
    duration: int


class OrderResponse(BaseModel):
    id: UUID4
    subscription_id: UUID4
    duration: int
    is_paid: bool


class SubscriptionResponse(BaseModel):
    id: UUID4
    expired_at: datetime
    tariff_id: UUID4
    company_id: UUID4
