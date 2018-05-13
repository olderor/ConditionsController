import base64
from datetime import datetime, timedelta
from hashlib import md5
import json
import os
from time import time
from flask import current_app, url_for
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import redis
import rq
import jwt
from app import db, login


class PaginatedAPIMixin(object):
    @staticmethod
    def to_collection_dict(query, page, per_page, endpoint, **kwargs):
        resources = query.paginate(page, per_page, False)
        data = {
            'items': [item.to_dict() for item in resources.items],
            '_meta': {
                'page': page,
                'per_page': per_page,
                'total_pages': resources.pages,
                'total_items': resources.total
            },
            '_links': {
                'self': url_for(endpoint, page=page, per_page=per_page,
                                **kwargs),
                'next': url_for(endpoint, page=page + 1, per_page=per_page,
                                **kwargs) if resources.has_next else None,
                'prev': url_for(endpoint, page=page - 1, per_page=per_page,
                                **kwargs) if resources.has_prev else None
            }
        }
        return data


class User(UserMixin, PaginatedAPIMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)
    role = db.Column(db.String(30))

    @staticmethod
    def get_by_email(email):
        return User.query.filter_by(email=email).first()

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'],
            algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

    def to_dict(self, include_email=False):
        data = {
            'id': self.id,
            'last_seen': self.last_seen.isoformat() + 'Z',
            'about_me': self.about_me,
            'role' : self.role
        }
        if include_email:
            data['email'] = self.email
        return data

    def from_dict(self, data, new_user=False):
        for field in ['email', 'about_me']:
            if field in data:
                setattr(self, field, data[field])
        if new_user and 'password' in data:
            self.set_password(data['password'])

    def set_role(self, role='client'):
        self.role = role

    def get_token(self, expires_in=3600000):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        return self.token

    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

    @staticmethod
    def check_token(token):
        user = User.query.filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        return user


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Organization(PaginatedAPIMixin, db.Model):
    __tablename__ = 'organization'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    about = db.Column(db.String(120))


class Storing(PaginatedAPIMixin, db.Model):
    __tablename__ = 'storing'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'))
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)


class ConditionField(PaginatedAPIMixin, db.Model):
    __tablename__ = 'condition_field'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    min_value = db.Column(db.Integer)
    max_value = db.Column(db.Integer)


class TrackingStatus(PaginatedAPIMixin, db.Model):
    __tablename__ = 'tracking_status'
    id = db.Column(db.Integer, primary_key=True)
    condition_id = db.Column(db.Integer, db.ForeignKey('condition.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    value = db.Column(db.Integer)
    date_recordered = db.Column(db.Integer, db.ForeignKey('product.id'))


class TrackingDevice(PaginatedAPIMixin, db.Model):
    __tablename__ = 'tracking_device'
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(120))
    token = db.Column(db.String(120))


class Product(PaginatedAPIMixin, db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    tracking_device_id = db.Column(db.Integer, db.ForeignKey('tracking_device.id'))
    product_type_id = db.Column(db.Integer, db.ForeignKey('product_types.id'))
    statuses = db.relationship('TrackingStatus', lazy='dynamic')

    @staticmethod
    def products_info():
        pass


class Condition(PaginatedAPIMixin, db.Model):
    __tablename__ = 'condition'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    min_value = db.Column(db.Integer)
    max_value = db.Column(db.Integer)
    product_type_id = db.Column(db.Integer, db.ForeignKey('product_types.id'))


class ProductType(PaginatedAPIMixin, db.Model):
    __tablename__ = 'product_types'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    expiration_date_length = db.Column(db.DateTime)
    description = db.Column(db.String(300))
    conditions = db.relationship('Condition', lazy='dynamic')
