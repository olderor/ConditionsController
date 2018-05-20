from app.organizations import bp
from flask import render_template, request


@bp.route('/', methods=['GET'])
def organizations():
    return render_template('organizations.html')


@bp.route('/get', methods=['GET'])
def organization():
    return render_template('organization.html')
