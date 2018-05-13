from app.users import bp
from flask import render_template, request
from flask_login import login_user
from flask_login import logout_user


@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    login_user(data['token'])


@bp.route('/logout', methods=['POST'])
def logout():
    logout_user()
