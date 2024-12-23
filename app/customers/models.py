from datetime import datetime
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


class Orders(Base):

    __tablename__ = 'order'

    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    duration: Mapped[int] = mapped_column(Integer, nullable=False)
    is_paid: Mapped[bool] = mapped_column(Boolean, nullable=False)


class Customers(Base):

    __tablename__ = 'customer'

    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    login: Mapped[str] = mapped_column(nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    phone: Mapped[str] = mapped_column(nullable=False)
    INN: Mapped[str] = mapped_column(nullable=False)
    address: Mapped[str] = mapped_column(nullable=False)

    session = relationship("Sessions", back_populates="customer", cascade="all, delete-orphan")

    def __str__(self):

        return f"Пользователь {self.login}"


class Sessions(Base):
    __tablename__ = 'sessions'

    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    jwt_token: Mapped[str] = mapped_column(nullable=False, unique=True)
    device: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    customer_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('customer.id', ondelete='CASCADE'), nullable=False)

    customer = relationship("Customers", back_populates="session")
