from app import create_app
from flask import g
from flask_user import current_user

app = create_app()


@app.before_request
def before_request():
    g.current_app = app
    g.current_user = current_user
