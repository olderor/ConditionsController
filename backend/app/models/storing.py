from app import db
from app.models.base import PaginatedAPIMixin


class Storing(PaginatedAPIMixin, db.Model):
    __tablename__ = 'storing'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'))
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
