# from fastapi import APIRouter, Depends, Request, Response
# from user_agents import parse

# from app.exceptions import (IncorrectEmailOrPasswordException,
#                             UserAlreadyExistsException)
# from app.customers.schemas import SUserAuth, TokenResponse
# from app.suppliers.auth import (authenticate_supplier,
#                                 create_access_token_supplier,
#                                 get_password_hash_supplier)
# from app.suppliers.dao import Sessions_supDAO, SuppliersDAO
# from app.suppliers.dependencies import get_current_supplier
# from app.suppliers.models import Suppliers
# from app.suppliers.schemas import SupplierRegister


# router = APIRouter(prefix="/supplier", tags=["Auth & Suppliers"])


# @router.post("/register")
# async def register(user_data: SupplierRegister) -> None:
#     existing_user = await SuppliersDAO.find_one_or_none(INN=user_data.INN)
#     if existing_user:
#         raise UserAlreadyExistsException

#     hashed_password = get_password_hash_supplier(user_data.password)

#     await SuppliersDAO.add(
#         name=user_data.name,
#         login=user_data.login,
#         hashed_password=hashed_password,
#         address=user_data.address,
#         phone=user_data.phone,
#         INN=user_data.INN
#     )


# @router.post("/login")
# async def login_user(
#       request: Request,
#       user_data: SUserAuth,
#       response: Response
#       ) -> TokenResponse:

#     supplier = await authenticate_supplier(
#         login=user_data.email,
#         password=user_data.password
#         )

#     if not supplier:

#         raise IncorrectEmailOrPasswordException
#     user_agent_str = request.headers.get("user-agent", "")
#     user_agent = parse(user_agent_str)
#     if user_agent.is_mobile:
#         device_type = "mobile"
#     elif user_agent.is_tablet:
#         device_type = "tablet"
#     else:
#         device_type = "desktop"

#     existing_session = await Sessions_supDAO.find_one_or_none(supplier_id=supplier.id, device=device_type)
#     if existing_session:
#         await Sessions_supDAO.delete_(model_id=existing_session.id)

#     access_token = create_access_token_supplier(
#         {"sub": str(supplier.id)}
#     )
#     await Sessions_supDAO.add(supplier_id=supplier.id, jwt_token=access_token, device=device_type)

#     response.set_cookie("access_token", access_token, httponly=True)
#     return TokenResponse(access_token=access_token)


# @router.post("/logout")
# async def logout_user(
#       request: Request,
#       response: Response,
#       supplier: Suppliers = Depends(get_current_supplier)
#       ) -> None:

#     user_agent_str = request.headers.get("user-agent", "")
#     user_agent = parse(user_agent_str)
#     if user_agent.is_mobile:
#         device_type = "mobile"
#     elif user_agent.is_tablet:
#         device_type = "tablet"
#     else:
#         device_type = "desktop"

#     existing_session = await Sessions_supDAO.find_one_or_none(supplier_id=supplier.id, device=device_type)
#     if existing_session:
#         await Sessions_supDAO.delete_(model_id=existing_session.id)

#     response.delete_cookie("access_token")
