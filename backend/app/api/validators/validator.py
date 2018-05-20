from functools import wraps
from flask import request
from app.api.controllers.errors import bad_request
from flask_babel import lazy_gettext as _l


class Validator:
    @staticmethod
    def validate(data, required_fields):
        result = {}
        for field in required_fields:
            if field not in data or not str(data[field]):
                return None
            result[field] = data[field]
        return result


def required_fields(fields):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            data = request.get_json() or {}
            data = Validator.validate(data, fields)
            if not data:
                return bad_request(101, _l('must include all required fields'))
            request.passed_data = data
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper
