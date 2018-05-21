from flask import jsonify, request, g
from app.models import Product
from app.api import bp
from app.api.auth import roled_login_required, token_auth
from app.api.validators.validator import required_fields
from app.api.controllers.errors import bad_request
from app.translate import translate as _l


@bp.route('/products', methods=['POST'])
@token_auth.login_required
@roled_login_required(roles=['manager', 'admin'])
@required_fields([], optional=['organization_id', 'product_type_id'])
def get_products():
    products = []
    if request.passed_data['product_type_id']:
        products = Product.get_products_by_product_type(request.passed_data['product_type_id'])
    elif request.passed_data['organization_id']:
        products = Product.get_products_by_organization(request.passed_data['organization_id'])
    elif g.current_user.role == 'admin':
        products = Product.get_products()

    response = jsonify({'products': [p.serialize(detailed=True) for p in products]})
    response.status_code = 200
    return response


@bp.route('/add-product', methods=['POST'])
@token_auth.login_required
@roled_login_required(roles=['manager', 'admin'])
@required_fields(['name', 'organization_id', 'product_type_id'])
def add_product():
    response = jsonify({'product': Product.add_product(request.passed_data).serialize()})
    response.status_code = 200
    return response


@bp.route('/product/get', methods=['POST'])
@required_fields(['product_id'])
def product_description():
    product = Product.get_product(request.passed_data['product_id'])
    if not product:
        return bad_request(103, _l('product is not found'))
    response = jsonify({'product': product.serialize(detailed=True, include_statuses=True)})
    response.status_code = 200
    return response


@bp.route('/product/assign-device', methods=['POST'])
@token_auth.login_required
@required_fields(['product_id', 'tracking_device_id'])
def product_assign_device():
    product = Product.get_product(request.passed_data['product_id'])
    if not product:
        return bad_request(103, _l('product is not found'))
    product.assign_tracking_device(request.passed_data['tracking_device_id'])
    response = jsonify({'product': product.serialize(detailed=True)})
    response.status_code = 200
    return response
