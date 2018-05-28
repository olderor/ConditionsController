from app import db
from app.models.base import PaginatedAPIMixin


class Condition(PaginatedAPIMixin, db.Model):
    __tablename__ = 'condition'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    description = db.Column(db.String(120))
    min_value = db.Column(db.Float)
    max_value = db.Column(db.Float)
    product_type_id = db.Column(db.Integer, db.ForeignKey('product_types.id'))
