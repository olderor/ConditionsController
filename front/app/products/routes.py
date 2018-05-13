from app.users import bp
from flask import render_template, request


@bp.route('/products', methods=['GET'])
def index():
    return render_template('products.html')
