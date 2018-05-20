from app.products import bp
from flask import render_template, request


@bp.route('/', methods=['GET'])
def products():
    return render_template('products.html')
