from app.dao.base import BaseDAO
from app.customers.models import Sessions, Users


class UsersDAO(BaseDAO):

    model = Users


class SessionsDAO(BaseDAO):

    model = Sessions
