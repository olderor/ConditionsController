from flask import jsonify, request
from app.logic.product_type import ProductType
from app.api.auth import bproute
from app.api.auth import roled_login_required, token_auth
from app.api.validators.validator import required_fields
from app.api.controllers.errors import bad_request
from app.translate import translate as _l


@bproute('/product-types')
@token_auth.login_required
@roled_login_required(roles=['manager', 'admin'])
@required_fields(['organization_id'])
def get_organization_product_types():
    product_types = ProductType.get_organization_product_types(request.passed_data['organization_id'])
    response = jsonify({'product_types': [p.serialize() for p in product_types]})
    response.status_code = 200
    return response


@bproute('/add-product-type')
@token_auth.login_required
@roled_login_required(roles=['manager', 'admin'])
@required_fields(['organization_id', 'expiration_date_length_hours', 'description', 'name', 'image_url'])
def add_product_type():
    response = jsonify({'product_type': ProductType.add_product_type(request.passed_data).serialize()})
    response.status_code = 200
    return response


@bproute('/product-type/get')
@token_auth.login_required
@roled_login_required(roles=['manager', 'admin'])
@required_fields(['product_type_id'])
def product_type_description():
    product_type = ProductType.get_product_type(request.passed_data['product_type_id'])
    if not product_type:
        return bad_request(103, _l('product type is not found'))
    response = jsonify({'product_type': product_type.serialize()})
    response.status_code = 200
    return response
