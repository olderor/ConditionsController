from flask import g
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from app.models import User, TrackingDevice
from app.api.controllers.errors import error_response
from functools import wraps


basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth('Bearer')
device_token_auth = HTTPTokenAuth('Bearer')


@basic_auth.verify_password
def verify_password(email, password):
    user = User.query.filter_by(email=email).first()
    if user is None:
        return False
    g.current_user = user
    return user.check_password(password)


@basic_auth.error_handler
def basic_auth_error():
    return error_response(401)


@token_auth.verify_token
def verify_token(token):
    g.current_user = User.check_token(token) if token else None
    return g.current_user is not None


@device_token_auth.verify_token
def verify_device_token(token):
    device = TrackingDevice.check_token(token) if token else None
    g.current_device = device
    return device is not None


@token_auth.error_handler
def token_auth_error():
    return error_response(401)


@device_token_auth.error_handler
def device_token_auth_error():
    return error_response(401)


def roled_login_required(roles=[]):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if g.current_user is None or not g.current_user.is_authenticated:
               return g.current_app.login_manager.unauthorized()
            urole = g.current_user.role
            if len(roles) == 0 and urole not in roles:
                return g.current_app.login_manager.unauthorized()
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper
