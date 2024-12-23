from app.dao.base import BaseDAO
from app.customers.models import Customers, Orders, Sessions


class CustomersDAO(BaseDAO):

    model = Customers


class SessionsDAO(BaseDAO):

    model = Sessions


class OrdersDAO(BaseDAO):

    model = Orders