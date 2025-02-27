from datetime import datetime, timedelta

from jose import JWTError, jwt
from passlib.context import CryptContext
from app.config import settings
from app.exceptions import TokenExpiredException
from app.customers.dao import CustomersDAO
from app.customers.models import Customers


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash_customer(password: str) -> str:

    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:

    return pwd_context.verify(plain_password, hashed_password)


def create_access_token_customer(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=90)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
        )
    return encoded_jwt


async def authenticate_customer(email: str, password: str) -> None | Customers:

    customer = await CustomersDAO.find_one_or_none(email=email)

    if not customer or not verify_password(password, customer.hashed_password):
        return None

    else:
        return customer


def verify_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM
            )
        return payload
    except JWTError:
        raise TokenExpiredException
