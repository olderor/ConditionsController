from app import db
from app.models.base import PaginatedAPIMixin


class TrackingDevice(PaginatedAPIMixin, db.Model):
    __tablename__ = 'tracking_device'
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(120))
    token = db.Column(db.String(120), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)
