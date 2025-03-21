from datetime import datetime
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


class Users(Base):

    __tablename__ = 'user'

    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    fio: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    phone: Mapped[str] = mapped_column(nullable=False)
    INN: Mapped[str] = mapped_column(nullable=False)
    address: Mapped[str] = mapped_column(nullable=False)
    is_customer: Mapped[bool] = mapped_column(Boolean, nullable=False)
    is_supplier: Mapped[bool] = mapped_column(Boolean, nullable=False)

    session = relationship("Sessions", back_populates="user", cascade="all, delete-orphan")
    carts = relationship("Carts", back_populates="user", cascade="all, delete-orphan")
    orders = relationship("Orders", back_populates="user", cascade="all, delete-orphan")
    roles = relationship("Roles", back_populates="user", cascade="all, delete-orphan")
    products = relationship("Products", back_populates="user", cascade="all, delete-orphan")

    def __str__(self):

        return f"Пользователь {self.login}"


class Sessions(Base):
    __tablename__ = 'sessions'

    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    jwt_token: Mapped[str] = mapped_column(nullable=False, unique=True)
    device: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    user_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('user.id', ondelete='CASCADE'), nullable=False)

    user = relationship("Users", back_populates="session")
