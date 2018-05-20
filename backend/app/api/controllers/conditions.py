from flask import jsonify, request
from app.api import bp
from app.models import Condition
from app.api.validators.validator import required_fields
from app.api.auth import roled_login_required


@bp.route('/conditions', methods=['POST'])
@required_fields(['product_type_id'])
def get_conditions():
    response = jsonify(Condition.get_conditions(request.passed_data['product_type_id']))
    response.status_code = 200
    return response


@bp.route('/add-condition', methods=['POST'])
@roled_login_required(roles=['manager', 'admin'])
@required_fields(['name', 'product_type_id', 'min_value', 'max_value'])
def add_condition():
    response = jsonify(Condition.add_conditions(request.passed_data))
    response.status_code = 200
    return response
