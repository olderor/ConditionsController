from app import create_app, db
from app.models import User
from flask import g, jsonify
from flask_login import current_user
from datetime import datetime

app = create_app()


@app.before_request
def before_request():
    g.current_user = current_user
    g.current_app = app


@app.after_request
def after_request(response):
    if g.current_user and g.current_user.is_authenticated:
        g.current_user.last_seen = datetime.utcnow()
        db.session.commit()
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response


@app.login_manager.unauthorized_handler
def unauth_handler():
    return jsonify(success=False,
                   data={'login_required': True},
                   message='Authorize please to access this page.'), 401


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User}
