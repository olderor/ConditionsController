from app import db
from app.models.base import *


class TrackingStatus(PaginatedAPIMixin, db.Model):
    __tablename__ = 'tracking_status'
    id = db.Column(db.Integer, primary_key=True)
    condition_id = db.Column(db.Integer, db.ForeignKey('condition.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    tracking_device_id = db.Column(db.Integer, db.ForeignKey('tracking_device.id'))
    value = db.Column(db.Float)
    date_recordered = db.Column(db.DateTime)
