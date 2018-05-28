from app import db
from app.models.base import PaginatedAPIMixin


class ProductType(PaginatedAPIMixin, db.Model):
    __tablename__ = 'product_types'
    id = db.Column(db.Integer, primary_key=True)
    organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'))
    name = db.Column(db.String(120))
    description = db.Column(db.String(300))
    image_url = db.Column(db.String(120))
    expiration_date_length_hours = db.Column(db.Integer)
