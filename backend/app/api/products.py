from flask import jsonify, g
from app import db
from app.api import bp
from app.api.auth import token_auth


@bp.route('/products', methods=['GET'])
@token_auth.login_required
def get_products():
    g.current_user
    db.session.commit()
    return '', 204

