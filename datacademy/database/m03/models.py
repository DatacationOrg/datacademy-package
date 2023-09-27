"""Module containing the database models for module 03."""

import datetime

from sqlalchemy import Date, Float, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, MappedAsDataclass, mapped_column, relationship


class Base(MappedAsDataclass, DeclarativeBase, repr=True):
    """Model base class."""


class Customer(Base):
    """Model for a customer."""

    __tablename__ = 'customers'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column(String)
    last_name: Mapped[str] = mapped_column(String)
    address: Mapped[str] = mapped_column(String)

    orders: Mapped[list['Order']] = relationship(back_populates='customer', init=False)

class Order(Base):
    """Model for an order."""

    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey('customers.id'))
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'))
    date: Mapped[datetime.date] = mapped_column(Date)
    quantity: Mapped[int] = mapped_column(Integer)

    customer: Mapped['Customer'] = relationship(back_populates='orders', init=False)
    product: Mapped['Product'] = relationship(back_populates='orders', init=False)

class Product(Base):
    """Model for a product."""

    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    price: Mapped[float] = mapped_column(Float)
    stock: Mapped[int] = mapped_column(Integer)

    orders: Mapped[list['Order']] = relationship(back_populates='product', init=False)
