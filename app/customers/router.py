from fastapi import APIRouter, Depends, Request, Response
from user_agents import parse

from app.exceptions import (IncorrectEmailOrPasswordException,
                            UserAlreadyExistsException)
from app.customers.auth import (authenticate_user, create_access_token,
                                get_password_hash)
from app.customers.dao import SessionsDAO, UsersDAO
from app.customers.dependencies import get_current_user
from app.customers.models import Users
from app.customers.schemas import SUserAuth, TokenResponse, UserRegister


router = APIRouter(prefix="/auth", tags=["Auth & Пользователи"])


@router.post("/register")
async def register(user_data: UserRegister) -> None:
    existing_user = await UsersDAO.find_one_or_none(INN=user_data.INN)
    if existing_user:
        raise UserAlreadyExistsException

    hashed_password = get_password_hash(user_data.password)

    await UsersDAO.add(
        fio=user_data.fio,
        email=user_data.email,
        hashed_password=hashed_password,
        address=user_data.address,
        phone=user_data.phone,
        INN=user_data.INN,
        is_customer=user_data.is_customer,
        is_supplier=user_data.is_supplier
    )


@router.post("/login")
async def login_user(
      request: Request,
      user_data: SUserAuth,
      response: Response
      ) -> TokenResponse:

    user = await authenticate_user(
        email=user_data.email,
        password=user_data.password
        )

    if not user:

        raise IncorrectEmailOrPasswordException
    user_agent_str = request.headers.get("user-agent", "")
    user_agent = parse(user_agent_str)
    if user_agent.is_mobile:
        device_type = "mobile"
    elif user_agent.is_tablet:
        device_type = "tablet"
    else:
        device_type = "desktop"

    existing_session = await SessionsDAO.find_one_or_none(user_id=user.id, device=device_type)
    if existing_session:
        await SessionsDAO.delete_(model_id=existing_session.id)

    access_token = create_access_token(
        {"sub": str(user.id)}
    )
    await SessionsDAO.add(user_id=user.id, jwt_token=access_token, device=device_type)

    response.set_cookie("access_token", access_token, httponly=True)
    return TokenResponse(access_token=access_token)


@router.post("/logout")
async def logout_user(
      request: Request,
      response: Response,
      user: Users = Depends(get_current_user)
      ) -> None:

    user_agent_str = request.headers.get("user-agent", "")
    user_agent = parse(user_agent_str)
    if user_agent.is_mobile:
        device_type = "mobile"
    elif user_agent.is_tablet:
        device_type = "tablet"
    else:
        device_type = "desktop"

    existing_session = await SessionsDAO.find_one_or_none(user_id=user.id, device=device_type)
    if existing_session:
        await SessionsDAO.delete_(model_id=existing_session.id)

    response.delete_cookie("access_token")
