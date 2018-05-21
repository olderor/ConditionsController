from app.product_types import bp
from flask import render_template


@bp.route('/', methods=['GET'])
def conditions():
    return render_template('product_types.html')


@bp.route('/get', methods=['GET'])
def condition():
    return render_template('product_types.html')
