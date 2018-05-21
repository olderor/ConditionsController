from flask import jsonify, request
from app.models import Condition
from app.api import bp
from app.api.auth import roled_login_required, token_auth
from app.api.validators.validator import required_fields


@bp.route('/conditions', methods=['POST'])
@token_auth.login_required
@roled_login_required(roles=['manager', 'admin'])
@required_fields(['product_type_id'])
def get_conditions():
    conditions = Condition.get_conditions(request.passed_data['product_type_id'])
    response = jsonify({'conditions': [c.serialize() for c in conditions]})
    response.status_code = 200
    return response


@bp.route('/add-condition', methods=['POST'])
@token_auth.login_required
@roled_login_required(roles=['manager', 'admin'])
@required_fields(['name', 'description', 'product_type_id'], optional=['min_value', 'max_value'])
def add_condition():
    condition = Condition.add_conditions(request.passed_data)
    response = jsonify({'condition': condition.serialize()})
    response.status_code = 200
    return response
