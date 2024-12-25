from datetime import datetime
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


class Suppliers(Base):

    __tablename__ = 'supplier'

    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    login: Mapped[str] = mapped_column(nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    phone: Mapped[str] = mapped_column(nullable=False)
    INN: Mapped[str] = mapped_column(nullable=False)
    address: Mapped[str] = mapped_column(nullable=False)

    session_sup = relationship("Sessions_sup", back_populates="supplier", cascade="all, delete-orphan")
    products = relationship("Products", back_populates="supplier", cascade="all, delete-orphan")

    def __str__(self):

        return f"Пользователь {self.login}"


class Sessions_sup(Base):
    __tablename__ = 'session_sup'

    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    jwt_token: Mapped[str] = mapped_column(nullable=False, unique=True)
    device: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    supplier_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('supplier.id', ondelete='CASCADE'), nullable=False)

    supplier = relationship("Suppliers", back_populates="session_sup")
