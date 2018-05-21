from app.products import bp
from flask import render_template


@bp.route('/', methods=['GET'])
def products():
    return render_template('products.html')


@bp.route('/get', methods=['GET'])
def product():
    return render_template('product.html')
