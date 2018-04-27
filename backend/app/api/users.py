from flask import jsonify, request, url_for
from app import db
from app.models import User
from app.api import bp
from app.api.auth import token_auth
from app.api.errors import bad_request


# @bp.route('/users/<int:id>', methods=['GET'])
# @token_auth.login_required
# def get_user(id):
#     return jsonify(User.query.get_or_404(id).to_dict())
#
#
# @bp.route('/users', methods=['GET'])
# @token_auth.login_required
# def get_users():
#     page = request.args.get('page', 1, type=int)
#     per_page = min(request.args.get('per_page', 10, type=int), 100)
#     data = User.to_collection_dict(User.query, page, per_page, 'api.get_users')
#     return jsonify(data)


@bp.route('/signup', methods=['POST'])
def create_user():
    data = request.get_json() or {}
    if 'email' not in data or 'password' not in data:
        return bad_request('must include email and password fields')
    if User.query.filter_by(email=data['email']).first():
        return bad_request('please use a different email address')
    user = User()
    user.roles = ['client']
    user.from_dict(data, new_user=True)
    db.session.add(user)
    db.session.commit()
    response = jsonify(user.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_user', id=user.id)
    return response
