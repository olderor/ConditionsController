from flask import jsonify, request, g
from app.models import TrackingDevice, Product, TrackingStatus
from app.api import bp
from app.api.controllers.errors import bad_request
from app.api.auth import roled_login_required, token_auth, device_token_auth
from app.translate import translate as _l
from app.api.validators.validator import required_fields, Validator


@bp.route('/login-device', methods=['POST'])
@required_fields(['key', 'password'])
def login_device():
    device = TrackingDevice.get_device(request.passed_data['key'])
    if not device or not device.check_password(request.passed_data['password']):
        return bad_request(103, _l('device is not found'))

    token = device.get_token()
    return jsonify({'token': token})


@bp.route('/register-device', methods=['POST'])
@token_auth.login_required
@roled_login_required(roles=['admin', 'manager'])
@required_fields(['key', 'password'])
def register_device():
    if TrackingDevice.get_device(request.passed_data['key']):
        return bad_request(102, _l('device is already registered'))

    TrackingDevice.add_device(request.passed_data)

    response = jsonify({'success': True})
    response.status_code = 200
    return response


@bp.route('/assign-device', methods=['POST'])
@token_auth.login_required
@roled_login_required(roles=['admin', 'manager'])
@required_fields(['key', 'password', 'product_id'])
def assign_device():
    device = TrackingDevice.get_device(request.passed_data['key'])
    if not device or not device.check_password(request.passed_data['password']):
        return bad_request(103, _l('device is not found'))

    product = Product.get_product(request.passed_data['product_id'])
    product.assign_tracking_device(device.id)

    response = jsonify({'success': True})
    response.status_code = 200
    return response


@bp.route('/track', methods=['POST'])
@device_token_auth.login_required
@required_fields(['value', 'condition_id', 'date_recordered'])
def track_status():
    request.passed_data.setdefault('tracking_device_id', g.current_device.id)
    TrackingStatus.add_status(request.passed_data)
    response = jsonify({'success': True})
    response.status_code = 200
    return response


@bp.route('/tracks', methods=['POST'])
@device_token_auth.login_required
@required_fields(['tracks'])
def track_statuses():
    tracks = []

    for track in request.passed_data['tracks']:
        track_data = Validator.validate(track, ['value', 'condition_id', 'date_recordered'], [])
        if not track_data:
            return bad_request(101, _l('must include all required fields'))
        tracks.append(track_data)

    for track in tracks:
        track.setdefault('tracking_device_id', g.current_device.id)
        TrackingStatus.add_status(track)

    response = jsonify({'success': True})
    response.status_code = 200
    return response
