from fastapi import APIRouter, Depends
from pydantic import UUID4
from app.base.dao import CartsDAO, Order_productsDAO, OrdersDAO, ProductsDAO, TariffsDAO, Warehouse_productsDAO, WarehousesDAO
from app.base.schemas import (CartsResponse, Order_productsResponse, OrdersResponse, ProductRequest, ProductResponse,
                              TariffRequest, TariffResponse, Warehouse_productResponse, WarehouseRequest, WarehouseResponse)
from app.customers.dependencies import get_current_customer
from app.exceptions import ProductNotFound, ProductOutOfStock, TariffNotFound
from app.suppliers.dependencies import get_current_supplier
from app.suppliers.models import Suppliers

router = APIRouter(prefix="/base", tags=["Base"])


@router.post("/add_product", description="Добавление товара")
async def add_product(
      product: ProductRequest,
      supplier: Suppliers = Depends(get_current_supplier)
      ) -> ProductResponse:
    result = await ProductsDAO.add(
        name=product.name,
        description=product.description,
        width=product.width,
        length=product.length,
        weight=product.weight,
        height=product.height,
        price=product.price,
        supplier_id=supplier.id
        )
    return ProductResponse(id=result.id,
                           name=result.name,
                           description=result.description,
                           width=result.width,
                           length=result.length,
                           weight=result.weight,
                           height=result.height,
                           price=result.price,
                           supplier_id=result.supplier_id)


@router.get("/products", description="Получение товаров продавца")
async def get_products_supplier(
      supplier: Suppliers = Depends(get_current_supplier)
      ) -> list[ProductResponse]:
    results = await ProductsDAO.find_all(supplier_id=supplier.id)
    if not results:
        raise ProductNotFound
    return [
        ProductResponse(id=result.id,
                        name=result.name,
                        description=result.description,
                        width=result.width,
                        length=result.length,
                        weight=result.weight,
                        height=result.height,
                        price=result.price,
                        supplier_id=result.supplier_id) for result in results]


@router.delete("/products/{product_id}", description="Удаление товара")
async def delete_product(
      product_id: UUID4,
      supplier: Suppliers = Depends(get_current_supplier)) -> None:
    await ProductsDAO.delete_(model_id=product_id)


@router.post("/add_warehouse", description="Добавление склада")
async def add_warehouse(
      warehouse: WarehouseRequest,
      supplier: Suppliers = Depends(get_current_supplier)
      ) -> WarehouseResponse:
    result = await WarehousesDAO.add(
        name=warehouse.name,
        address=warehouse.address,
        )
    return WarehouseResponse(id=result.id,
                             name=result.name,
                             address=result.address)


@router.get("/warehouses", description="Получение складов")
async def get_warehouses(
      supplier: Suppliers = Depends(get_current_supplier)
      ) -> list[WarehouseResponse]:
    results = await WarehousesDAO.find_all()
    if not results:
        raise ProductNotFound
    return [
        WarehouseResponse(id=result.id,
                          name=result.name,
                          address=result.address) for result in results]


@router.delete("/warehouses/{warehouse_id}", description="Удаление склада")
async def delete_warehouse(
      warehouse_id: UUID4,
      supplier: Suppliers = Depends(get_current_supplier)) -> None:
    await WarehousesDAO.delete_(model_id=warehouse_id)


@router.post("/add_warehouse_product")
async def add_warehouse_product(
      warehouse_id: UUID4,
      product_id: UUID4,
      quantity: int,
      supplier: Suppliers = Depends(get_current_supplier)
      ) -> Warehouse_productResponse:
    product = await ProductsDAO.find_by_id(product_id)
    if product.supplier_id != supplier.id:
        raise ProductNotFound
    result = await Warehouse_productsDAO.add(
        product_id=product_id,
        quantity=quantity,
        warehouse_id=warehouse_id
        )
    return Warehouse_productResponse(id=result.id,
                                     product_id=result.product_id,
                                     warehouse_id=result.warehouse_id,
                                     quantity=result.quantity,
                                     update_date=result.update_date)


@router.get("/products_on_warehouse")
async def get_warehouse_products(
      warehouse_id: UUID4,
      supplier: Suppliers = Depends(get_current_supplier)
      ) -> list[Warehouse_productResponse]:
    results = await Warehouse_productsDAO.find_all(warehouse_id=warehouse_id)
    response_data = []
    for result in results:
        supplier_product = await ProductsDAO.find_by_id(result.product_id)
        if supplier_product.supplier_id != supplier.id:
            raise ProductNotFound
        response_data.append(Warehouse_productResponse(id=result.id,
                                                       product_id=result.product_id,
                                                       warehouse_id=result.warehouse_id,
                                                       quantity=result.quantity,
                                                       update_date=result.update_date))
    return response_data


@router.get("/product_on_warehouses")
async def get_warehouses_product(
      product_id: UUID4,
      supplier: Suppliers = Depends(get_current_supplier)
      ) -> list[Warehouse_productResponse]:
    results = await Warehouse_productsDAO.find_all(product_id=product_id)
    return [
        Warehouse_productResponse(id=result.id,
                                  product_id=result.product_id,
                                  warehouse_id=result.warehouse_id,
                                  quantity=result.quantity,
                                  update_date=result.update_date) for result in results]


@router.delete("/warehouse_products/{warehouse_product_id}")
async def delete_warehouse_product(
      warehouse_product_id: UUID4,
      supplier: Suppliers = Depends(get_current_supplier)) -> None:
    await Warehouse_productsDAO.delete_(model_id=warehouse_product_id)

@router.post("/add_product_to_cart")
async def add_product_to_cart(
      warehouse_product_id: UUID4,
      quantity: int,
      customer: Suppliers = Depends(get_current_customer)
      ) -> CartsResponse:
    product = await Warehouse_productsDAO.find_by_id(warehouse_product_id)
    if not product:
        raise ProductNotFound
    if quantity > product.quantity:
        raise ProductOutOfStock
    result = await CartsDAO.add(
        quantity=quantity,
        customer_id=customer.id,
        warehouse_product_id=warehouse_product_id
        )
    return CartsResponse(id=result.id,
                         warehouse_product_id=result.warehouse_product_id,
                         customer_id=result.customer_id,
                         quantity=result.quantity)


@router.get("/carts")
async def get_carts(
      customer: Suppliers = Depends(get_current_customer)
      ) -> list[CartsResponse]:
    results = await CartsDAO.find_all(customer_id=customer.id)
    return [
        CartsResponse(id=result.id,
                      warehouse_product_id=result.warehouse_product_id,
                      customer_id=result.customer_id,
                      quantity=result.quantity) for result in results]


@router.delete("/carts/{cart_id}")
async def delete_cart(
      cart_id: UUID4,
      customer: Suppliers = Depends(get_current_customer)) -> None:
    await CartsDAO.delete_(model_id=cart_id)


@router.post("/add_order")
async def add_order(
      customer: Suppliers = Depends(get_current_customer)
      ) -> OrdersResponse:
    results = await CartsDAO.find_all(customer_id=customer.id)
    if not results:
        raise ProductNotFound
    order_data = []
    total_price = 0
    order = await OrdersDAO.add(
        status="Ожидает оплаты",
        customer_id=customer.id
    )
    for result in results:
        warehouse_product = await Warehouse_productsDAO.find_by_id(result.warehouse_product_id)
        product = await ProductsDAO.find_by_id(warehouse_product.product_id)
        if result.quantity > warehouse_product.quantity:
            raise ProductOutOfStock
        total_price += product.price * result.quantity
        order_product = await Order_productsDAO.add(
            quantity=result.quantity,
            order_id=order.id,
            warehouse_product_id=result.warehouse_product_id
        )
        order_data.append(
            Order_productsResponse(
                id=order_product.id,
                order_id=order_product.order_id,
                warehouse_product_id=order_product.warehouse_product_id,
                quantity=order_product.quantity
            )
        )
        await CartsDAO.delete_(model_id=result.id)
    order = await OrdersDAO.update_(model_id=order.id,
                                    total_price=total_price)
    return OrdersResponse(
        id=order.id,
        total_price=order.total_price,
        products=order_data,
        created_at=order.created_at,
        updated_at=order.updated_at,
        status=order.status
    )


@router.get("/orders")
async def get_orders(
      customer: Suppliers = Depends(get_current_customer)
      ) -> list[OrdersResponse]:
    orders = await OrdersDAO.find_all(customer_id=customer.id)
    orders_data = []
    for order in orders:
        order_data = []
        results = await Order_productsDAO.find_all(order_id=order.id)
        for result in results:
            order_data.append(
              Order_productsResponse(
                  id=result.id,
                  order_id=result.order_id,
                  warehouse_product_id=result.warehouse_product_id,
                  quantity=result.quantity
              )
            )
        orders_data.append(
            OrdersResponse(
                id=order.id,
                total_price=order.total_price,
                products=order_data,
                created_at=order.created_at,
                updated_at=order.updated_at,
                status=order.status
            )
        )

    return orders_data


# @router.post("/tariff", description="Добавление тарифа в библиотеку")
# async def add_tariff(
#       data: TariffRequest,
#       user: Users = Depends(get_current_user)
#       ) -> TariffResponse:
#     tariff = await TariffsDAO.add(
#         name=data.name,
#         limit_users=data.limit_users,
#         price=data.price
#     )
#     return TariffResponse(
#         id=tariff.id,
#         name=tariff.name,
#         limit_users=tariff.limit_users,
#         price=tariff.price
#     )


# @router.get("/tariff", description="Получение тарифов из библиотеки")
# async def get_tariffs(
#       user: Users = Depends(get_current_user)
#       ) -> list[TariffResponse]:
#     tariffs = await TariffsDAO.find_all()
#     if not tariffs:
#         raise TariffNotFound
#     return [
#         TariffResponse(
#             id=tariff.id,
#             name=tariff.name,
#             limit_users=tariff.limit_users,
#             price=tariff.price
#         ) for tariff in tariffs
#     ]
