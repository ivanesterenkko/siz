from app.dao.base import BaseDAO
from app.customers.models import Customers, Sessions


class CustomersDAO(BaseDAO):

    model = Customers


class SessionsDAO(BaseDAO):

    model = Sessions
