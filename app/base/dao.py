from app.base.models import Carts, Order_products, Orders, Products, Tariffs, Warehouses, Warehouses_products
from app.dao.base import BaseDAO


class ProductsDAO(BaseDAO):

    model = Products


class WarehousesDAO(BaseDAO):

    model = Warehouses


class Warehouse_productsDAO(BaseDAO):

    model = Warehouses_products


class CartsDAO(BaseDAO):

    model = Carts


class OrdersDAO(BaseDAO):

    model = Orders


class Order_productsDAO(BaseDAO):

    model = Order_products


class TariffsDAO(BaseDAO):

    model = Tariffs
