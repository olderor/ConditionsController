from flask import jsonify, request
from app.models import User, Organization
from app.api import bp
from app.api.auth import roled_login_required, token_auth
from app.api.validators.validator import required_fields
from app.api.controllers.errors import bad_request
from app.translate import translate as _l
from app import db


@bp.route('/organization/get', methods=['POST'])
@token_auth.login_required
@roled_login_required(roles=['admin'])
@required_fields(['organization_id'])
def organization_description():
    organization = Organization.get_organization(request.passed_data['organization_id'])
    if not organization:
        return bad_request(103, _l('organization is not found'))
    response = jsonify({'organization': organization.serialize()})
    response.status_code = 200
    return response


@bp.route('/organization/change-status', methods=['POST'])
@token_auth.login_required
@roled_login_required(roles=['admin'])
@required_fields(['organization_id', 'active'])
def organization_change_status():
    organization = Organization.get_organization(request.passed_data['organization_id'])
    if not organization:
        return bad_request(103, _l('organization is not found'))
    organization.disabled = request.passed_data['active'] == False
    db.session.commit()
    response = jsonify({'organization': organization.serialize()})
    response.status_code = 200
    return response


@bp.route('/organization/users', methods=['POST'])
@token_auth.login_required
@roled_login_required(roles=['manager', 'admin'])
@required_fields(['organization_id'])
def organization_users():
    users = User.get_by_organization(request.passed_data['organization_id'])
    response = jsonify({'users': [u.serialize(include_email=True) for u in users]})
    response.status_code = 200
    return response


@bp.route('/organization/register', methods=['POST'])
@token_auth.login_required
@roled_login_required(roles=['admin'])
@required_fields(['email', 'password', 'organization_id', 'name', 'image_url', 'description'])
def organization_register():
    if User.query.filter_by(email=request.passed_data['email']).first():
        return bad_request(102, _l('please use a different email address'))

    request.passed_data.setdefault('role', 'manager')

    user = User()
    user.from_dict(request.passed_data, new_user=True)
    db.session.add(user)
    db.session.commit()

    response = jsonify(user.serialize())
    response.status_code = 200
    return response
