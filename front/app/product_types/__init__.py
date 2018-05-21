from flask import Blueprint

bp = Blueprint('product_types', __name__, url_prefix='/product_types')

from app.product_types import routes