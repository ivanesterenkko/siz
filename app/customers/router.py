from fastapi import APIRouter, Depends, Request, Response
from user_agents import parse

from app.exceptions import (IncorrectEmailOrPasswordException,
                            UserAlreadyExistsException)
from app.customers.auth import (authenticate_customer,
                                create_access_token_customer,
                                get_password_hash_customer)
from app.customers.dao import CustomersDAO, SessionsDAO
from app.customers.dependencies import get_current_customer
from app.customers.models import Customers
from app.customers.schemas import CustomerRegister, SUserAuth, TokenResponse


router = APIRouter(prefix="/auth", tags=["Auth & Пользователи"])


@router.post("/register")
async def register(user_data: CustomerRegister) -> None:
    existing_user = await CustomersDAO.find_one_or_none(INN=user_data.INN)
    if existing_user:
        raise UserAlreadyExistsException

    hashed_password = get_password_hash_customer(user_data.password)

    await CustomersDAO.add(
        fio=user_data.fio,
        email=user_data.email,
        hashed_password=hashed_password,
        address=user_data.address,
        phone=user_data.phone,
        INN=user_data.INN
    )


@router.post("/login")
async def login_user(
      request: Request,
      user_data: SUserAuth,
      response: Response
      ) -> TokenResponse:

    customer = await authenticate_customer(
        email=user_data.email,
        password=user_data.password
        )

    if not customer:

        raise IncorrectEmailOrPasswordException
    user_agent_str = request.headers.get("user-agent", "")
    user_agent = parse(user_agent_str)
    if user_agent.is_mobile:
        device_type = "mobile"
    elif user_agent.is_tablet:
        device_type = "tablet"
    else:
        device_type = "desktop"

    existing_session = await SessionsDAO.find_one_or_none(customer_id=customer.id, device=device_type)
    if existing_session:
        await SessionsDAO.delete_(model_id=existing_session.id)

    access_token = create_access_token_customer(
        {"sub": str(customer.id)}
    )
    await SessionsDAO.add(customer_id=customer.id, jwt_token=access_token, device=device_type)

    response.set_cookie("access_token", access_token, httponly=True)
    return TokenResponse(access_token=access_token)


@router.post("/logout")
async def logout_user(
      request: Request,
      response: Response,
      customer: Customers = Depends(get_current_customer)
      ) -> None:

    user_agent_str = request.headers.get("user-agent", "")
    user_agent = parse(user_agent_str)
    if user_agent.is_mobile:
        device_type = "mobile"
    elif user_agent.is_tablet:
        device_type = "tablet"
    else:
        device_type = "desktop"

    existing_session = await SessionsDAO.find_one_or_none(customer_id=customer.id, device=device_type)
    if existing_session:
        await SessionsDAO.delete_(model_id=existing_session.id)

    response.delete_cookie("access_token")
