from app.base.models import Addresses, Attribute_values, Attributes, Carts, Categories, Order_products, Orders, Product_attributes, Products, Role_classes, Roles, Tariffs, Warehouses, Warehouses_products
from app.dao.base import BaseDAO


class ProductsDAO(BaseDAO):

    model = Products


class WarehousesDAO(BaseDAO):

    model = Warehouses


class Warehouse_productsDAO(BaseDAO):

    model = Warehouses_products


class CategoriesDAO(BaseDAO):

    model = Categories


class AttributesDAO(BaseDAO):

    model = Attributes


class Attributes_valueDAO(BaseDAO):

    model = Attribute_values


class Product_attributesDAO(BaseDAO):

    model = Product_attributes


class CartsDAO(BaseDAO):

    model = Carts


class OrdersDAO(BaseDAO):

    model = Orders


class Order_productsDAO(BaseDAO):

    model = Order_products


class TariffsDAO(BaseDAO):

    model = Tariffs


class RolesDAO(BaseDAO):

    model = Roles


class Role_classesDAO(BaseDAO):

    model = Role_classes


class AddressesDAO(BaseDAO):

    model = Addresses