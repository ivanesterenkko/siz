from datetime import datetime

from fastapi import Depends, HTTPException, Request
from jose import JWTError, jwt

from app.config import settings
from app.customers.models import Customers
from app.exceptions import (IncorrectTokenFormatException,
                            TokenAbsentException, TokenExpiredException,
                            UserIsNotPresentException)
from app.customers.dao import CustomersDAO, SessionsDAO


def get_token(request: Request):

    token = (
        request.cookies.get("access_token")
        or request.headers.get("Authorization")
    )

    if not token:
        raise TokenAbsentException

    if token.startswith("Bearer "):
        token = token[len("Bearer "):]

    return token


async def get_current_customer(token: str = Depends(get_token)):

    try:

        payload = jwt.decode(
            token, settings.SECRET_KEY, settings.ALGORITHM
        )

    except JWTError:

        raise IncorrectTokenFormatException

    expire = payload.get("exp")

    if (not expire) or (int(expire) < datetime.utcnow().timestamp()):

        raise TokenExpiredException

    customer_id = payload.get("sub")

    if not customer_id:

        raise UserIsNotPresentException

    customer = await CustomersDAO.find_by_id(customer_id)

    if not customer:
        raise UserIsNotPresentException

    session = await SessionsDAO.find_one_or_none(jwt_token=token)

    if not session:
        raise HTTPException(status_code=401, detail="Token mismatch")

    return customer
