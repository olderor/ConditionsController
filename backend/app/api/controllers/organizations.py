from flask import jsonify, request
from app.models import Organization
from app.api import bp
from app.api.auth import roled_login_required, token_auth
from app.api.validators.validator import required_fields


@bp.route('/organizations', methods=['POST'])
@token_auth.login_required
@roled_login_required(roles=['admin'])
def get_organizations():
    response = jsonify({'organizations': [o.serialize() for o in Organization.get_organizations()]})
    response.status_code = 200
    return response


@bp.route('/add-organization', methods=['POST'])
@token_auth.login_required
@roled_login_required(roles=['admin'])
@required_fields(['name', 'about', 'image_url'])
def add_organization():
    response = jsonify({'organization': Organization.add_organization(request.passed_data).serialize()})
    response.status_code = 200
    return response
