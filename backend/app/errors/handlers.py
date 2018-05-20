from flask import request
from app import db
from app.errors import bp
from app.api.controllers.errors import error_response as api_error_response


def wants_json_response():
    return request.accept_mimetypes['application/json'] >= \
        request.accept_mimetypes['text/html']


@bp.app_errorhandler(404)
def not_found_error(error):
    return api_error_response(404)


@bp.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return api_error_response(500)
