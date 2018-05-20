from flask import jsonify, g, request
from app.api import bp
from app.api.auth import token_auth
from app.models import Product, ProductType
from app.api.auth import roled_login_required
from app.api.validators.validator import required_fields


@bp.route('/product-types', methods=['POST'])
@token_auth.login_required
@roled_login_required(roles=['admin'])
def get_product_types():
    response = jsonify({'product_types': [pt.serialize() for pt in ProductType.get_product_types()]})
    response.status_code = 200
    return response


@bp.route('/products', methods=['POST'])
@token_auth.login_required
@roled_login_required(roles=['admin'])
def get_products():
    response = jsonify(Product.get_products())
    response.status_code = 200
    return response

