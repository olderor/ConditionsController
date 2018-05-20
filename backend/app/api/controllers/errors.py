from flask import jsonify


def error_response(status_code, message=None):
    payload = {'error': message}
    response = jsonify(payload)
    response.status_code = status_code
    return response


def bad_request(error_code, message):
    return error_response(200, message)
