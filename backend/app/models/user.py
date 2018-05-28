from datetime import datetime
from flask_login import UserMixin
from app import db
from app.models.base import PaginatedAPIMixin


class User(UserMixin, PaginatedAPIMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)
    role = db.Column(db.String(30))
    disabled = db.Column(db.Boolean, default=False)
    organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'), nullable=True)
    image_url = db.Column(db.String(120))
    name = db.Column(db.String(120))
    description = db.Column(db.String(120))
