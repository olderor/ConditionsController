from app import db
from app.models.base import PaginatedAPIMixin


class Organization(PaginatedAPIMixin, db.Model):
    __tablename__ = 'organization'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    about = db.Column(db.String(120))
    image_url = db.Column(db.String(120))
    disabled = db.Column(db.Boolean, default=False)
