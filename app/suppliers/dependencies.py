from datetime import datetime

from fastapi import Depends, HTTPException, Request
from jose import JWTError, jwt

from app.config import settings
from app.exceptions import (IncorrectTokenFormatException,
                            TokenAbsentException, TokenExpiredException,
                            UserIsNotPresentException)
from app.suppliers.dao import Sessions_supDAO, SuppliersDAO


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


async def get_current_supplier(token: str = Depends(get_token)):

    try:

        payload = jwt.decode(
            token, settings.SECRET_KEY, settings.ALGORITHM
        )

    except JWTError:

        raise IncorrectTokenFormatException

    expire = payload.get("exp")

    if (not expire) or (int(expire) < datetime.utcnow().timestamp()):

        raise TokenExpiredException

    supplier_id = payload.get("sub")

    if not supplier_id:

        raise UserIsNotPresentException

    supplier = await SuppliersDAO.find_by_id(supplier_id)

    if not supplier:
        raise UserIsNotPresentException

    session = await Sessions_supDAO.find_one_or_none(jwt_token=token)

    if not session:
        raise HTTPException(status_code=401, detail="Token mismatch")

    return supplier
