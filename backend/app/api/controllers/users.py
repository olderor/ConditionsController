from flask import jsonify, request, g
from app import db
from app.logic.user import User
from app.api.auth import bproute
from app.api.controllers.errors import bad_request
from app.api.auth import roled_login_required, token_auth
from app.translate import translate as _l
from app.api.validators.validator import required_fields


@bproute('/login')
@required_fields(['email', 'password'])
def login():
    user = User.get_by_email(request.passed_data['email'])
    if not user or not user.check_password(request.passed_data['password']):
        return bad_request(103, _l('user is not found'))
    g.current_user = user

    token = user.get_token()
    db.session.commit()
    return jsonify({'token': token, 'role': user.role, 'email': user.email, 'organization_id': user.organization_id})


@bproute('/signup')
@required_fields(['email', 'password'])
def signup():
    if User.get_by_email(request.passed_data['email']):
        return bad_request(102, _l('please use a different email address'))

    user = User()
    user.from_dict(request.passed_data, new_user=True)
    user.role = 'admin'
    db.session.add(user)
    db.session.commit()

    response = jsonify(user.serialize())
    response.status_code = 200
    return response


@bproute('/register')
@token_auth.login_required
@roled_login_required(roles=['admin'])
@required_fields(['email', 'password'])
def register():
    if User.get_by_email(request.passed_data['email']):
        return bad_request(102, _l('please use a different email address'))

    request.passed_data.setdefault('role', 'client')

    user = User()
    user.from_dict(request.passed_data, new_user=True)
    db.session.add(user)
    db.session.commit()

    response = jsonify(user.serialize())
    response.status_code = 200
    return response


@bproute('/change-status')
@token_auth.login_required
@roled_login_required(roles=['admin'])
@required_fields(['user_id', 'active'])
def change_status():
    user = User.get_user(request.passed_data['user_id'])
    if not user:
        return bad_request(103, _l('user is not found'))
    user.disabled = request.passed_data['active'] == False
    db.session.commit()
    response = jsonify({'user': user.serialize()})
    response.status_code = 200
    return response
