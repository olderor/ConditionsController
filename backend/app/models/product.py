from app import db
from app.models.base import *


class Product(PaginatedAPIMixin, db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'))
    product_type_id = db.Column(db.Integer, db.ForeignKey('product_types.id'))
    tracking_device_id = db.Column(db.Integer, db.ForeignKey('tracking_device.id'))
    date_created = db.Column(db.DateTime)
    status = db.Column(db.String(120))
    # statuses = db.relationship('TrackingStatus', lazy='dynamic')
