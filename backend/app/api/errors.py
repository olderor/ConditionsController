from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES


def error_response(status_code, error_code=None, message=None):
    payload = {'error': HTTP_STATUS_CODES.get(status_code, 'Unknown error')}
    if message:
        payload['message'] = message
    if error_code:
        payload['error_code'] = error_code
    response = jsonify(payload)
    response.status_code = status_code
    return response


def bad_request(error_code, message):
    return error_response(200, error_code, message)
