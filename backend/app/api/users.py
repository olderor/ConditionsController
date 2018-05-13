from flask import jsonify, request, url_for, redirect, g
from flask_login import login_user
from app import db
from app.models import User
from app.api import bp
from app.api.errors import bad_request
from app.api.auth import login_required, token_auth


@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    if 'email' not in data or 'password' not in data:
        return bad_request(101, 'must include email and password fields')

    user = User.get_by_email(data['email'])
    if not user or not user.check_password(data['password']):
        return bad_request(103, 'user is not found')
    g.current_user = user

    token = g.current_user.get_token()
    db.session.commit()
    return jsonify({'token': token})


@bp.route('/signup', methods=['POST'])
def create_user():
    data = request.get_json() or {}
    if 'email' not in data or 'password' not in data:
        return bad_request(101, 'must include email and password fields')
    if User.get_by_email(data['email']):
        return bad_request(102, 'please use a different email address')
    user = User()
    user.from_dict(data, new_user=True)
    user.set_role('client')
    db.session.add(user)
    db.session.commit()
    response = jsonify(user.to_dict())
    response.status_code = 200
    return response


@bp.route('/signup-admin', methods=['POST'])
@token_auth.verify_token
@login_required(roles=['admin'])
def create_user_admin():
    data = request.get_json() or {}
    if 'email' not in data or 'password' not in data:
        return bad_request(101, 'must include email and password fields')
    if User.query.filter_by(email=data['email']).first():
        return bad_request(102, 'please use a different email address')
    data.setdefault('role', 'client')
    user = User()
    user.from_dict(data, new_user=True)
    user.set_role(data['role'])
    db.session.add(user)
    db.session.commit()
    response = jsonify(user.to_dict())
    response.status_code = 200
    return response
