from fastapi import APIRouter, Depends, Request, Response
from user_agents import parse

from app.exceptions import (IncorrectEmailOrPasswordException,
                            UserAlreadyExistsException)
from app.customers.auth import (authenticate_customer, create_access_token,
                            get_password_hash)
from app.customers.dao import CustomersDAO, SessionsDAO
from app.customers.dependencies import get_current_customer
from app.customers.models import Customers
from app.customers.schemas import SAdminRegister, SUserAuth, TokenResponse


router = APIRouter(prefix="/customer", tags=["Auth & Customers"])


@router.post("/register")
async def register(user_data: SAdminRegister) -> None:
    existing_user = await CustomersDAO.find_one_or_none(INN=user_data.INN)
    if existing_user:
        raise UserAlreadyExistsException

    hashed_password = get_password_hash(user_data.password)

    await CustomersDAO.add(
        name=user_data.name,
        login=user_data.login,
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
        login=user_data.login,
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

    access_token = create_access_token(
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
