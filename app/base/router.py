from typing import Dict
from fastapi import APIRouter, Depends
from pydantic import UUID4
from app.base.dao import AddressesDAO, Attributes_valueDAO, AttributesDAO, CartsDAO, CategoriesDAO, EmployeesDAO, IssuancesDAO, Product_attributesDAO, Product_itemsDAO, ProductsDAO, Role_classesDAO, RolesDAO, Warehouse_productsDAO, WarehousesDAO
from app.base.schemas import (AddProductRequest, AddWarehouse_itemRequest, AddWarehouseResponse, AddressesRequest, Attribute_valuiesIDRequest, Attribute_valuiesRequest, Attribute_valuiesResponse, AttributesIDRequest, AttributesRequest, AttributesResponse, CartResponse, CartsResponse, CategoryIDRequest, CategoryRequest, CategoryResponse, ClassTypesResponse, ClassesResponse, EmployeeComResponse, EmployeeRequest, EmployeeResponse, IssuanceEmplResponse, IssuanceRequest, IssuanceResponse, NewEmployeeResponse, Product_attributeResponse, Product_itemEmpResponse, Product_itemRequest, Product_itemResponse, ProductAttributesResponse, ProductCategoryResponse, ProductEmpResponse, ProductRequest, ProductResponse, QuantityRequest, Role_classesPutRequest, Role_classesRequest, Role_classesResponse, RoleClassesCatResponse, RolesRequest, RolesResponse,
                              Warehouse_productResponse, WarehouseComResponse, WarehouseGetProductComResponse, WarehouseGetProductResponse, WarehouseGetResponse, WarehousePatchRequest, WarehouseRequest, WarehouseResponse)
from app.customers.dependencies import get_current_user
from app.customers.models import Users
from app.exceptions import ProductNotFound

router = APIRouter()


@router.post("/products", description="Добавление товара", tags=["Внутренняя"])
async def add_product(
      product: ProductRequest,
      user: Users = Depends(get_current_user)
      ) -> None:
    await ProductsDAO.add(
        name=product.name,
        description=product.description,
        width=product.width,
        length=product.length,
        weight=product.weight,
        height=product.height,
        price=product.price,
        user_id=user.id,
        color=product.color,
        country=product.country,
        brand=product.brand,
        gost=product.gost,
        article=product.article,
        lifespan=product.lifespan,
        produce_time=product.produce_time,
        is_by_order=product.is_by_order,
        category_id=product.class_id,
        product_category=product.category
        )
    return None


@router.get("/catalog/{class_type}/{class_id}", description="Получение списка товаров в категории", tags=["Products"])
async def get_products(
      class_type: str,
      class_id: UUID4,
      user: Users = Depends(get_current_user)
      ) -> list[ProductResponse]:
    result_response = []
    results = await ProductsDAO.find_all(category_id=class_id)
    classes = await CategoriesDAO.find_by_id(class_id)
    classes_response = ClassesResponse(
        id=classes.id,
        name=classes.name,
        type=classes.type
    )
    if not results:
        raise ProductNotFound
    for result in results:
        product_attributes = []
        attributes = await Product_attributesDAO.find_all(product_id=result.id)
        for attribute in attributes:
            attribute_or = await AttributesDAO.find_by_id(attribute.attribute_id)
            value = await Attributes_valueDAO.find_by_id(attribute.attribute_value_id)
            product_attributes.append(
                Product_attributeResponse(
                    id=attribute.id,
                    attribute_id=attribute.attribute_id,
                    name=attribute_or.name,
                    value_id=value.id,
                    value=value.name
                )
            )
        result_response.append(
            ProductResponse(
                id=result.id,
                user_id=result.user_id,
                name=result.name,
                description=result.description,
                price=result.price,
                classes=classes_response,
                category=result.product_category,
                color=result.color,
                article=result.article,
                brand=result.brand,
                gost=result.gost,
                is_by_order=result.is_by_order,
                produce_time=result.produce_time,
                country=result.country,
                lifespan=result.lifespan,
                width=result.width,
                weight=result.weight,
                length=result.length,
                height=result.height,
                items_available=None,
                pictures=None,
                certificates=None,
                attributes=product_attributes
            )
        )
    return result_response


@router.get("/catalog/{class_type}/{class_id}/{product_id}", description="Получение товара по id", tags=["Product"])
async def get_product(
      class_type: str,
      class_id: UUID4,
      product_id: UUID4,
      user: Users = Depends(get_current_user)
      ) -> ProductResponse:
    result = await ProductsDAO.find_by_id(product_id)
    classes = await CategoriesDAO.find_by_id(class_id)
    classes_response = ClassesResponse(
        id=classes.id,
        name=classes.name,
        type=classes.type
    )
    if not result:
        raise ProductNotFound
    product_attributes = []
    attributes = await Product_attributesDAO.find_all(product_id=result.id)
    for attribute in attributes:
        attribute_or = await AttributesDAO.find_by_id(attribute.attribute_id)
        value = await Attributes_valueDAO.find_by_id(attribute.attribute_value_id)
        product_attributes.append(
            Product_attributeResponse(
                id=attribute.id,
                attribute_id=attribute.attribute_id,
                name=attribute_or.name,
                value_id=value.id,
                value=value.name
            )
        )
    return ProductResponse(
        id=result.id,
        user_id=result.user_id,
        name=result.name,
        description=result.description,
        price=result.price,
        classes=classes_response,
        category=result.product_category,
        color=result.color,
        article=result.article,
        brand=result.brand,
        gost=result.gost,
        is_by_order=result.is_by_order,
        produce_time=result.produce_time,
        country=result.country,
        lifespan=result.lifespan,
        width=result.width,
        weight=result.weight,
        length=result.length,
        height=result.height,
        items_available=None,
        pictures=None,
        certificates=None,
        attributes=product_attributes
    )


@router.delete("/catalog/{class_type}/{class_id}/{product_id}", description="Удаление товара", tags=["Product"])
async def delete_product(
      class_type: str,
      class_id: UUID4,
      product_id: UUID4,
      user: Users = Depends(get_current_user)) -> None:
    await ProductsDAO.delete_(model_id=product_id)


@router.post("/catalog/{class_type}/{class_id}/{product_id}", description="Добавление товара в корзину", tags=["Product"])
async def add_product_to_cart(
      class_type: str,
      class_id: UUID4,
      product_id: UUID4,
      quantity: QuantityRequest,
      user: Users = Depends(get_current_user)
      ) -> CartResponse:
    result = await CartsDAO.add(
        quantity=quantity,
        user_id=user.id,
        product_id=product_id
        )
    return CartResponse(product_cart_id=result.id)


@router.post("/warehouses", description="Добавление склада", tags=["Warehouse"])
async def add_warehouse(
      warehouse: WarehouseRequest,
      user: Users = Depends(get_current_user)
      ) -> AddWarehouseResponse:
    address = await AddressesDAO.add(
        region=warehouse.address.region,
        city=warehouse.address.city,
        street=warehouse.address.street,
        house=warehouse.address.house,
        building=warehouse.address.building,
        structure=warehouse.address.structure,
        flat=warehouse.address.flat
    )
    result = await WarehousesDAO.add(
        name=warehouse.name,
        phone=warehouse.phone,
        representative_name=warehouse.representativeName,
        address_id=address.id,
        )
    return AddWarehouseResponse(
        warehouse_id=result.id,
        name=result.name,
        datetime_created=result.datetime_created,
        address_id=result.address_id)


@router.get("/warehouses", description="Получение складов", tags=["Warehouse"])
async def get_warehouses(
      user: Users = Depends(get_current_user)
      ) -> list[WarehouseResponse]:
    results = await WarehousesDAO.find_all()
    if not results:
        raise ProductNotFound
    warehouse_response = []
    for result in results:
        address = await AddressesDAO.find_by_id(result.address_id)
        warehouse_response.append(
            WarehouseResponse(
                id=result.id,
                name=result.name,
                phone=result.phone,
                representativeName=result.representative_name,
                address_id=result.address_id,
                address=AddressesRequest(
                    region=address.region,
                    city=address.city,
                    street=address.street,
                    house=address.house,
                    building=address.building,
                    structure=address.structure,
                    flat=address.flat
                )
            )
        )
    return warehouse_response


@router.get("/warehouses/{warehouse_id}", description="Получение склада", tags=["Warehouse"])
async def get_warehouse(
      warehouse_id: UUID4,
      user: Users = Depends(get_current_user)
      ) -> WarehouseResponse:
    result = await WarehousesDAO.find_by_id(warehouse_id)
    if not result:
        raise ProductNotFound
    address = await AddressesDAO.find_by_id(result.address_id)
    return WarehouseResponse(
        id=result.id,
        name=result.name,
        phone=result.phone,
        representativeName=result.representative_name,
        address_id=result.address_id,
        address=AddressesRequest(
            region=address.region,
            city=address.city,
            street=address.street,
            house=address.house,
            building=address.building,
            structure=address.structure,
            flat=address.flat
        )
    )


@router.patch("/warehouses/{warehouse_id}", description="Изменение информации о складе", tags=["Warehouse"])
async def patch_warehouse(
      warehouse_id: UUID4,
      warehouse: WarehousePatchRequest,
      user: Users = Depends(get_current_user)
      ) -> WarehouseResponse:
    result = await WarehousesDAO.find_by_id(warehouse_id)
    if not result:
        raise ProductNotFound
    result = await WarehousesDAO.update_(
        model_id=warehouse_id,
        name=warehouse.name,
        phone=warehouse.phone,
        representative_name=warehouse.representativeName,
        )
    address = await AddressesDAO.update_(
        model_id=warehouse.address_id,
        region=warehouse.address.region,
        city=warehouse.address.city,
        street=warehouse.address.street,
        house=warehouse.address.house,
        building=warehouse.address.building,
        structure=warehouse.address.structure,
        flat=warehouse.address.flat
    )
    return WarehouseResponse(
        id=result.id,
        name=result.name,
        phone=result.phone,
        representativeName=result.representative_name,
        address_id=result.address_id,
        address=AddressesRequest(
            region=address.region,
            city=address.city,
            street=address.street,
            house=address.house,
            building=address.building,
            structure=address.structure,
            flat=address.flat
        )
    )

@router.delete("/warehouses/{warehouse_id}", description="Удаление склада", tags=["Warehouse"])
async def delete_warehouse(
      warehouse_id: UUID4,
      user: Users = Depends(get_current_user)) -> None:
    await WarehousesDAO.delete_(model_id=warehouse_id)


@router.post("/warehouses/{warehouse_id}/add_role", tags=["Roles"])
async def add_role(
      warehouse_id: UUID4,
      role: RolesRequest,
      user: Users = Depends(get_current_user)
      ):
    result = await RolesDAO.add(
        user_id=user.id,
        name=role.name,
        description=role.description,
        warehouse_id=warehouse_id
        )
    return {"role_id": result.id}


@router.get("/warehouses/{warehouse_id}/{role_id}", tags=["Roles"])
async def get_role(
      warehouse_id: UUID4,
      role_id: UUID4,
      user: Users = Depends(get_current_user)
      ) -> RolesResponse:
    role = await RolesDAO.find_by_id(role_id)
    role_classes = await Role_classesDAO.find_all(role_id=role_id)
    warehouse = await WarehousesDAO.find_by_id(warehouse_id)
    sum_price = 0
    emp_info = []
    employees = await EmployeesDAO.find_all(role_id=role_id)
    for employee in employees:
        emp_info.append(
            EmployeeResponse(
                id=employee.id,
                name=employee.name,
                gender=employee.gender,
                role=RolesResponse(
                    id=role.id,
                    name=role.name,
                    description=role.description
                ),
                is_archive=employee.is_archive,
                size_clothes=employee.size_clothes,
                size_shoes=employee.size_shoes,
                height=employee.height,
                length=employee.length,
                size_head=employee.size_head
            )
        )
    complectation = []
    for role_class in role_classes:
        if role_class.product_id is None:
            continue
        product = await ProductsDAO.find_by_id(role_class.product_id)
        sum_price += product.price
        product_items = await Product_itemsDAO.find_all(product_id=product.id)
        classes = await CategoriesDAO.find_by_id(product.category_id)
        classes_res = ClassesResponse(
            id=classes.id,
            type=classes.type,
            name=classes.name
        )
        items = []
        for product_item in product_items:
            warehouse_item = await Warehouse_productsDAO.find_one_or_none(product_item_id=product_item.id)
            product_item = await Product_itemsDAO.find_by_id(warehouse_item.product_item_id)
            items.append(WarehouseGetResponse(
                id=product_item.id,
                size=product_item.size,
                man_size=product_item.man_size,
                woman_size=product_item.woman_size,
                quantity=warehouse_item.quantity
            )
            )
        product_res = WarehouseGetProductResponse(
                    id=product.id,
                    role_class_id=role_class.id,
                    name=product.name,
                    price=product.price,
                    items=items
                )
        complectation.append(WarehouseGetProductComResponse(
            role_class_id=role_class.id,
            classes=classes_res,
            product=product_res
        ))
    return WarehouseComResponse(
        name=warehouse.name,
        price_role=sum_price,
        info=emp_info,
        complectation=complectation
    )


@router.patch("/warehouses/{warehouse_id}/{role_id}", tags=["Roles"])
async def patch_role(
      warehouse_id: UUID4,
      role_id: UUID4,
      role: RolesRequest,
      user: Users = Depends(get_current_user)
      ) -> RolesResponse:
    result = await RolesDAO.update_(
        model_id=role_id,
        name=role.name,
        description=role.description
        )
    return RolesResponse(
        id=result.id,
        name=result.name,
        description=result.description
    )


@router.delete("/warehouses/{warehouse_id}/{role_id}", tags=["Roles"])
async def delete_role(
      warehouse_id: UUID4,
      role_id: UUID4,
      user: Users = Depends(get_current_user)
      ) -> None:
    await RolesDAO.delete_(model_id=role_id)


@router.post("/warehouses/{warehouse_id}/{role_id}/add_role_class", tags=["Roles"])
async def add_role_class(
      warehouse_id: UUID4,
      role_id: UUID4,
      role_class: Role_classesRequest,
      user: Users = Depends(get_current_user)
      ):
    result = await Role_classesDAO.add(
        role_id=role_id,
        name=role_class.category,
        lifespan=role_class.lifespan,
        category_id=role_class.class_id
        )
    product_attributes = []
    for atr in role_class.product_attrubutes:
        res_atr = await Product_attributesDAO.add(
            attribute_id=atr.attribute_id,
            attribute_value_id=atr.attribute_value_id,
            role_class_id=result.id
        )
        product_attributes.append(
            ProductAttributesResponse(
                id=res_atr.id
            )
        )
    return Role_classesResponse(
        id=result.id,
        product_attrubutes=product_attributes
    )


@router.put("/warehouses/{warehouse_id}/{role_id}/{role_class_id}", tags=["Roles"])
async def put_role_class(
      warehouse_id: UUID4,
      role_id: UUID4,
      role_class: Role_classesPutRequest,
      role_class_id: UUID4,
      user: Users = Depends(get_current_user)
      ) -> Role_classesResponse:
    result = await Role_classesDAO.update_(
        model_id=role_class_id,
        role_id=role_id,
        name=role_class.category,
        lifespan=role_class.lifespan,
        category_id=role_class.class_id
        )
    product_attributes = []
    for atr in role_class.product_attrubutes:
        res_atr = await Product_attributesDAO.update_(
            model_id=atr.id,
            attribute_id=atr.attribute_id,
            attribute_value_id=atr.attribute_value_id,
            role_class_id=result.id
        )
        product_attributes.append(
            ProductAttributesResponse(
                id=res_atr.id
            )
        )
    return Role_classesResponse(
        id=result.id,
        product_attrubutes=product_attributes
    )


@router.get("/warehouses/{warehouse_id}/roles/{role_id}/{role_class_id}", tags=["Roles"])
async def get_product_to_role_class(
      warehouse_id: UUID4,
      role_id: UUID4,
      role_class_id: UUID4,
      user: Users = Depends(get_current_user)
      ) -> list[ProductResponse]:
    role_class = await Role_classesDAO.find_by_id(role_class_id)
    results = await ProductsDAO.find_all(category_id=role_class.category_id)
    result_response = []
    classes = await CategoriesDAO.find_by_id(role_class.category_id)
    classes_response = ClassesResponse(
        id=classes.id,
        name=classes.name,
        type=classes.type
    )
    if not results:
        raise ProductNotFound
    for result in results:
        product_attributes = []
        attributes = await Product_attributesDAO.find_all(product_id=result.id)
        if attributes is None:
            product_attributes = None
        else:
            for attribute in attributes:
                attribute_or = await AttributesDAO.find_by_id(attribute.attribute_id)
                value = await Attributes_valueDAO.find_by_id(attribute.attribute_value_id)
                product_attributes.append(
                    Product_attributeResponse(
                        id=attribute.id,
                        attribute_id=attribute.attribute_id,
                        name=attribute_or.name,
                        value_id=value.id,
                        value=value.name
                    )
                )
        item_response = []
        product_items = await Product_itemsDAO.find_all(prodcut_id=result.id)
        if product_items is None:
            item_response = None
        else:
            for product_item in product_items:
                warehouse_item = await Warehouse_productsDAO.find_one_or_none(
                    product_item_id=product_item.id
                )
                item_response.append(
                    Product_itemResponse(
                        id=product_item.id,
                        size=product_item.size,
                        man_size=product_item.man_size,
                        woman_size=product_item.woman_size,
                        warehouse_item_id=warehouse_item.id,
                        quantity=warehouse_item.quantity
                    )
                )
        result_response.append(
            ProductResponse(
                id=result.id,
                supplier_id=result.supplier_id,
                name=result.name,
                description=result.description,
                price=result.price,
                classes=classes_response,
                category=result.product_category,
                color=result.color,
                article=result.article,
                brand=result.brand,
                gost=result.gost,
                is_by_order=result.is_by_order,
                produce_time=result.produce_time,
                country=result.country,
                lifespan=result.lifespan,
                width=result.width,
                weight=result.weight,
                length=result.length,
                height=result.height,
                items_available=item_response,
                pictures=None,
                certificates=None,
                attributes=product_attributes
            )
        )
    return result_response



@router.delete("/warehouses/{warehouse_id}/{role_id}/{role_class_id}", tags=["Roles"])
async def delete_role_class(
      warehouse_id: UUID4,
      role_id: UUID4,
      role_class_id: UUID4,
      user: Users = Depends(get_current_user)
      ) -> None:
    await RolesDAO.delete_(model_id=role_class_id)

@router.patch("/warehouses/{warehouse_id}/roles/{role_id}/{role_class_id}", tags=["Roles"])
async def add_product_to_role_class(
      warehouse_id: UUID4,
      role_id: UUID4,
      role_class_id: UUID4,
      product: AddProductRequest,
      user: Users = Depends(get_current_user)
      ) -> AddProductRequest:
    result = await Role_classesDAO.update_(
        model_id=role_class_id,
        product_id=product.product_id
        )
    return AddProductRequest(product_id=result.product_id)


@router.post("/warehouses/{warehouse_id}/roles/{role_id}/add_employee", tags=["Roles"])
async def add_employee(
      warehouse_id: UUID4,
      role_id: UUID4,
      employee: EmployeeRequest,
      user: Users = Depends(get_current_user)
      ) -> NewEmployeeResponse:
    result = await EmployeesDAO.add(
        role_id=role_id,
        name=employee.name,
        gender=employee.gender,
        is_archive=employee.is_archive,
        size_clothes=employee.size_clothes,
        size_shoes=employee.size_shoes,
        height=employee.height,
        length=employee.length,
        size_head=employee.size_head
        )
    return NewEmployeeResponse(
        id=result.id,
        created_at=result.created_at
    )


@router.get("/warehouses/{warehouse_id}/roles/{role_id}/{employee_id}")
async def get_employee(
      warehouse_id: UUID4,
      role_id: UUID4,
      employee_id: UUID4,
      user: Users = Depends(get_current_user)
      ) -> EmployeeComResponse:
    employee = await EmployeesDAO.find_by_id(employee_id)
    role = await RolesDAO.find_by_id(employee.role_id)
    issuances = await IssuancesDAO.find_all(employee_id=employee_id)
    if issuances is None:
        status = None
        date_at = None
        complectation = None
    else:
        status = "Укомплектован"
        date_at = issuances[0].date_at
        complectation = []
        for issuance in issuances:
            warehouse_item = await Warehouse_productsDAO.find_by_id(issuance.warehouse_product_id)
            product_item = await Product_itemsDAO.find_by_id(warehouse_item.product_item_id)
            product = await ProductsDAO.find_by_id(product_item.product_id)
            classes = await CategoriesDAO.find_by_id(product.category_id)
            classes_res = ClassesResponse(
                id=classes.id,
                type=classes.type,
                name=classes.name
            )
            product_res = ProductEmpResponse(
                id=product.id,
                name=product.name,
                price=product.price,
                item=Product_itemEmpResponse(
                    id=product_item.id,
                    size=product_item.size,
                    man_size=product_item.man_size,
                    woman_size=product_item.woman_size
                )
            )
            complectation.append(IssuanceEmplResponse(
                role_class_id=issuance.role_class_id,
                classes=classes_res,
                product=product_res
            ))
    employee_info = EmployeeResponse(
        id=employee.id,
        name=employee.name,
        gender=employee.gender,
        role=RolesResponse(
            id=role.id,
            name=role.name,
            description=role.description
        ),
        is_archive=employee.is_archive,
        size_clothes=employee.size_clothes,
        size_shoes=employee.size_shoes,
        height=employee.height,
        length=employee.length,
        size_head=employee.size_head
    )
    return EmployeeComResponse(
        status=status,
        date_at=date_at,
        info=employee_info,
        complectation=complectation
    )


@router.patch("/warehouses/{warehouse_id}/roles/{role_id}/{employee_id}", tags=["Roles"])
async def patch_employee(
      warehouse_id: UUID4,
      role_id: UUID4,
      employee_id: UUID4,
      employee: EmployeeRequest,
      user: Users = Depends(get_current_user)
      ) -> EmployeeResponse:
    result = await EmployeesDAO.update_(
        model_id=employee_id,
        role_id=role_id,
        name=employee.name,
        gender=employee.gender,
        is_archive=employee.is_archive,
        size_clothes=employee.size_clothes,
        size_shoes=employee.size_shoes,
        height=employee.height,
        length=employee.length,
        size_head=employee.size_head
        )
    role = await RolesDAO.find_by_id(role_id)
    return EmployeeResponse(
        id=result.id,
        name=result.name,
        role=RolesResponse(
            id=role.id,
            name=role.name,
            description=role.description
        ),
        gender=result.gender,
        is_archive=result.is_archive,
        size_clothes=result.size_clothes,
        size_shoes=result.size_shoes,
        height=result.height,
        length=result.length,
        size_head=result.size_head
    )


@router.delete("/warehouses/{warehouse_id}/roles/{role_id}/{employee_id}", tags=["Roles"])
async def delete_employee(
      warehouse_id: UUID4,
      role_id: UUID4,
      employee_id: UUID4,
      user: Users = Depends(get_current_user)
      ) -> None:
    await EmployeesDAO.delete_(employee_id)


@router.post("/warehouses/{warehouse_id}/add_issuances", tags=["Roles"])
async def add_issuance(
      warehouse_id: UUID4,
      issuances: IssuanceRequest,
      user: Users = Depends(get_current_user)
      ) -> list[IssuanceResponse]:
    response = []
    for issuance in issuances.warehouse_items:
        result = await IssuancesDAO.add(
            quantity=issuance.quantity,
            warehouse_product_id=issuance.warehouse_product_id,
            role_class_id=issuance.role_class_id,
            type=issuances.type,
            employee_id=issuances.employee_id,
            comment=issuances.comment
        )
        response.append(
            IssuanceResponse(
                id=result.id,
                date_at=result.date_at
            )
        )
    return response


@router.post("/warehouses/{warehouse_id}/add_warehouse_product", tags=["Warehouse"])
async def add_warehouse_product(
      warehouse_id: UUID4,
      product_item: AddWarehouse_itemRequest,
      user: Users = Depends(get_current_user)
      ) -> None:
    await Warehouse_productsDAO.add(
        warehouse_id=warehouse_id,
        product_item_id=product_item.product_item_id,
        quantity=product_item.quantity
    )
    return None


@router.patch("/warehouses/{warehouse_id}/{warehouse_item_id}", tags=["Warehouse"])
async def get_warehouse_products(
      warehouse_id: UUID4,
      warehouse_item_id: UUID4,
      quantity: QuantityRequest,
      user: Users = Depends(get_current_user)
      ) -> QuantityRequest:
    result = await Warehouse_productsDAO.update_(
        model_id=warehouse_item_id,
        quantity=quantity.quantity
        )
    return QuantityRequest(
        quantity=result.quantity
    )


@router.get("/product_on_warehouses", tags=["Внутренняя"])
async def get_warehouses_product(
      product_id: UUID4,
      user: Users = Depends(get_current_user)
      ) -> list[Warehouse_productResponse]:
    results = await Warehouse_productsDAO.find_all(product_id=product_id)
    return [
        Warehouse_productResponse(id=result.id,
                                  product_id=result.product_id,
                                  warehouse_id=result.warehouse_id,
                                  quantity=result.quantity,
                                  update_date=result.update_date) for result in results]


@router.delete("/warehouses/{warehouse_id}/{warehouse_item_id}", tags=["Warehouse"])
async def delete_warehouse_product(
      warehouse_product_id: UUID4,
      user: Users = Depends(get_current_user)) -> None:
    await Warehouse_productsDAO.delete_(model_id=warehouse_product_id)


@router.post("/add_categories", description="Добавление категории", tags=["Внутренняя"])
async def add_categories(
      categories: list[CategoryRequest],
      user: Users = Depends(get_current_user)
      ) -> None:
    for category in categories:
        await CategoriesDAO.add(
            name=category.name,
            type=category.type
            )
    return None


@router.post("/add_categories_with_id", description="Добавление категории", tags=["Внутренняя"])
async def add_categories_id(
      categories: list[CategoryIDRequest],
      user: Users = Depends(get_current_user)
      ) -> None:
    for category in categories:
        await CategoriesDAO.add(
            id=category.id,
            name=category.name,
            type=category.type
            )
    return None


@router.get("/catalog_types", tags=["Products"])
async def get_categories(
      user: Users = Depends(get_current_user)
      ) -> list[ClassTypesResponse]:
    class_dict: Dict[str, int] = {}
    classes = await CategoriesDAO.find_all()
    response_data = []
    for class_e in classes:
        if str(class_e.type) not in class_dict:
            class_dict[str(class_e.type)] = 0
        class_dict[str(class_e.type)] += 1
    for key, value in class_dict.items():
        response_data.append(
            ClassTypesResponse(
                type=key,
                count_classes=value
            )
        )
    return response_data


@router.get("/catalog/{class_type}", tags=["Products"])
async def get_categories_type(
      class_type: str,
      user: Users = Depends(get_current_user)
      ) -> list[CategoryResponse]:
    classes = await CategoriesDAO.find_all(type=class_type)
    response_data = []
    for class_e in classes:
        products = await ProductsDAO.find_all(category_id=class_e.id)
        response_data.append(
            CategoryResponse(
                name=class_e.name,
                id=class_e.id,
                count_products=len(products)
            )
        )
    return response_data


@router.get("/{class_id}/attributes_values", description="Характеристики для класса товара", tags=["Attributies by category"])
async def get_attributies(
      class_id: UUID4,
      user: Users = Depends(get_current_user)
      ) -> list[AttributesResponse]:
    attributies = await AttributesDAO.find_all(category_id=class_id)
    attribute_response = []
    for attribute in attributies:
        attribute_values = await Attributes_valueDAO.find_all(attribute_id=attribute.id)
        atr_value_response = []
        for atr_value in attribute_values:
            atr_value_response.append(
                Attribute_valuiesResponse(
                    id=atr_value.id,
                    name=atr_value.name
                )
            )
        attribute_response.append(
            AttributesResponse(
                id=attribute.id,
                name=attribute.name,
                is_protection=attribute.is_protection,
                attribute_values=atr_value_response
            )
        )
    return attribute_response


@router.get("/{class_id}/product_categories", description="Категории для класса товара", tags=["Categories by category"])
async def get_categories_by_class(
      class_id: UUID4,
      user: Users = Depends(get_current_user)
      ) -> list[ProductCategoryResponse]:
    products = await AttributesDAO.find_all(category_id=class_id)
    categories_response = []
    for product in products:
        if product.product_category is None:
            continue
        categories_response.append(str(product.product_category))
    categories_response = list(set(categories_response))
    return categories_response


@router.get("/{role_id}/role_classes", description="Категории снаряженич для должности", tags=["Role classes by role"])
async def get_classes_by_role(
      role_id: UUID4,
      user: Users = Depends(get_current_user)
      ) -> list[RoleClassesCatResponse]:
    role_classes = await AttributesDAO.find_all(role_id=role_id)
    response = []
    for role_class in role_classes:
        category = await CategoriesDAO.find_by_id(role_class.category_id)
        response.append(
            RoleClassesCatResponse(
                id=role_class.id,
                classes=ClassesResponse(
                    id=category.id,
                    type=category.type,
                    name=category.name
                )
            )
        )
    return response


@router.delete("/classes/{class_id}", tags=["Внутренняя"])
async def delete_category(
      class_id: UUID4,
      user: Users = Depends(get_current_user)) -> None:
    await CategoriesDAO.delete_(model_id=class_id)


@router.post("/add_attributies", description="Добавление хакактеристики", tags=["Внутренняя"])
async def add_attributies(
      attributies: list[AttributesRequest],
      user: Users = Depends(get_current_user)
      ) -> None:
    for attribute in attributies:
        await AttributesDAO.add(
            name=attribute.name,
            is_protection=attribute.is_protection,
            category_id=attribute.class_id
            )
    return None


@router.post("/add_attributies_with_id", description="Добавление хакактеристики", tags=["Внутренняя"])
async def add_attributies_id(
      attributies: list[AttributesIDRequest],
      user: Users = Depends(get_current_user)
      ) -> None:
    for attribute in attributies:
        await AttributesDAO.add(
            id=attribute.id,
            name=attribute.name,
            is_protection=attribute.is_protection,
            category_id=attribute.class_id
            )
    return None


@router.post("/add_attribute_values", description="Добавление хакактеристики", tags=["Внутренняя"])
async def add_attribute_values(
      attribute_values: list[Attribute_valuiesRequest],
      user: Users = Depends(get_current_user)
      ) -> None:
    for attribute in attribute_values:
        await Attributes_valueDAO.add(
            name=attribute.name,
            attribute_id=attribute.attribute_id
            )
    return None


@router.post("/add_attribute_values_with_id", description="Добавление хакактеристики", tags=["Внутренняя"])
async def add_attribute_values_id(
      attribute_values: list[Attribute_valuiesIDRequest],
      user: Users = Depends(get_current_user)
      ) -> None:
    for attribute in attribute_values:
        await Attributes_valueDAO.add(
            id=attribute.id,
            name=attribute.name,
            attribute_id=attribute.attribute_id
            )
    return None


@router.delete("/classes/{class_id}/attributes/{attribute_id}", tags=["Внутренняя"])
async def delete_attribute(
      attribute_id: UUID4,
      user: Users = Depends(get_current_user)) -> None:
    await AttributesDAO.delete_(model_id=attribute_id)


@router.post("/products/{product_id}/add_product_item", description="Добавление размеров для товара", tags=["ProductItems"])
async def add_product_item(
      product_id: UUID4,
      product_item: Product_itemRequest,
      user: Users = Depends(get_current_user)
      ) -> None:
    await Product_itemsDAO.add(
        product_id=product_id,
        size=product_item.size,
        man_size=product_item.man_size,
        woman_size=product_item.woman_size
    )
    return None


@router.delete("/products/{product_id}/{product_item_id}", tags=["ProductItems"])
async def delete_product_item(
      product_id: UUID4,
      product_item_id: UUID4,
      user: Users = Depends(get_current_user)) -> None:
    await Product_itemsDAO.delete_(model_id=product_item_id)


# @router.post("/add_product_to_cart")
# async def add_product_to_cart(
#       warehouse_product_id: UUID4,
#       quantity: int,
#       user: Users = Depends(get_current_user)
#       ) -> CartsResponse:
#     product = await Warehouse_productsDAO.find_by_id(warehouse_product_id)
#     if not product:
#         raise ProductNotFound
#     if quantity > product.quantity:
#         raise ProductOutOfStock
#     result = await CartsDAO.add(
#         quantity=quantity,
#         customer_id=customer.id,
#         warehouse_product_id=warehouse_product_id
#         )
#     return CartsResponse(id=result.id,
#                          warehouse_product_id=result.warehouse_product_id,
#                          customer_id=result.customer_id,
#                          quantity=result.quantity)


@router.get("/cart", tags=["Cartффф"])
async def get_cart(
      user: Users = Depends(get_current_user)
      ) -> list[CartsResponse]:
    results = await CartsDAO.find_all(user_id=user.id)
    return [
        CartsResponse(id=result.id,
                      warehouse_product_id=result.warehouse_product_id,
                      user_id=result.user_id,
                      quantity=result.quantity) for result in results]


@router.delete("/carts/{cart_id}")
async def delete_cart(
      cart_id: UUID4,
      user: Users = Depends(get_current_user)) -> None:
    await CartsDAO.delete_(model_id=cart_id)


# @router.post("/add_order")
# async def add_order(
#       user: Users = Depends(get_current_user)
#       ) -> OrdersResponse:
#     results = await CartsDAO.find_all(customer_id=customer.id)
#     if not results:
#         raise ProductNotFound
#     order_data = []
#     total_price = 0
#     order = await OrdersDAO.add(
#         status="Ожидает оплаты",
#         customer_id=customer.id
#     )
#     for result in results:
#         warehouse_product = await Warehouse_productsDAO.find_by_id(result.warehouse_product_id)
#         product = await ProductsDAO.find_by_id(warehouse_product.product_id)
#         if result.quantity > warehouse_product.quantity:
#             raise ProductOutOfStock
#         total_price += product.price * result.quantity
#         order_product = await Order_productsDAO.add(
#             quantity=result.quantity,
#             order_id=order.id,
#             warehouse_product_id=result.warehouse_product_id
#         )
#         order_data.append(
#             Order_productsResponse(
#                 id=order_product.id,
#                 order_id=order_product.order_id,
#                 warehouse_product_id=order_product.warehouse_product_id,
#                 quantity=order_product.quantity
#             )
#         )
#         await CartsDAO.delete_(model_id=result.id)
#     order = await OrdersDAO.update_(model_id=order.id,
#                                     total_price=total_price)
#     return OrdersResponse(
#         id=order.id,
#         total_price=order.total_price,
#         products=order_data,
#         created_at=order.created_at,
#         updated_at=order.updated_at,
#         status=order.status
#     )


# @router.get("/orders")
# async def get_orders(
#       user: Users = Depends(get_current_user)
#       ) -> list[OrdersResponse]:
#     orders = await OrdersDAO.find_all(customer_id=customer.id)
#     orders_data = []
#     for order in orders:
#         order_data = []
#         results = await Order_productsDAO.find_all(order_id=order.id)
#         for result in results:
#             order_data.append(
#               Order_productsResponse(
#                   id=result.id,
#                   order_id=result.order_id,
#                   warehouse_product_id=result.warehouse_product_id,
#                   quantity=result.quantity
#               )
#             )
#         orders_data.append(
#             OrdersResponse(
#                 id=order.id,
#                 total_price=order.total_price,
#                 products=order_data,
#                 created_at=order.created_at,
#                 updated_at=order.updated_at,
#                 status=order.status
#             )
#         )

#     return orders_data


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
