import base64
from datetime import datetime, timedelta
import os
from time import time
from flask import current_app, url_for
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from app import db, login
from dateutil.parser import parse as datetime_parse
from app.translate import translate as _l


STATUS_EXPIRED = 'expired'
STATUS_SPOILED = 'spoiled'
STATUS_NEW = 'new'
FAIL_STATUSES = [STATUS_EXPIRED, STATUS_SPOILED]


class PaginatedAPIMixin(object):
    @staticmethod
    def to_collection_dict(query, page, per_page, endpoint, **kwargs):
        resources = query.paginate(page, per_page, False)
        data = {
            'items': [item.serialize() for item in resources.items],
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
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)
    role = db.Column(db.String(30))
    disabled = db.Column(db.Boolean, default=False)
    organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'), nullable=True)
    image_url = db.Column(db.String(120))
    name = db.Column(db.String(120))
    description = db.Column(db.String(120))

    def is_disabled(self):
        if self.disabled:
            return True
        return False

    @staticmethod
    def get_user(id):
        return User.query.filter_by(id=id).first()

    @staticmethod
    def get_by_email(email):
        return User.query.filter_by(email=email).first()

    @staticmethod
    def get_by_organization(organization_id):
        return list(reversed(User.query.filter_by(organization_id=organization_id).all()))

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

    def serialize(self, include_email=False):
        data = {
            'id': self.id,
            'last_seen': self.last_seen.isoformat() + 'Z',
            'role' : self.role,
            'organization_id': self.organization_id,
            'disabled': self.is_disabled(),
            'image_url': self.image_url,
            'name': self.name,
            'description': self.description
        }
        if include_email:
            data['email'] = self.email
        return data

    def from_dict(self, data, new_user=False):
        for field in ['email', 'organization_id', 'name', 'image_url', 'description', 'role']:
            if field in data:
                setattr(self, field, data[field])
        if new_user and 'password' in data:
            self.set_password(data['password'])

    def get_token(self, expires_in=3600000):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.commit()
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
    image_url = db.Column(db.String(120))
    disabled = db.Column(db.Boolean, default=False)

    def is_disabled(self):
        if self.disabled:
            return True
        return False

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'about': self.about,
            'image_url': self.image_url,
            'disabled': self.is_disabled()
        }

    @staticmethod
    def get_organizations():
        return list(reversed(Organization.query.all()))

    @staticmethod
    def get_organization(id):
        return Organization.query.filter_by(id=id).first()

    @staticmethod
    def add_organization(data):
        organization = Organization()
        organization.name = data['name']
        organization.about = data['about']
        organization.image_url = data['image_url']
        db.session.add(organization)
        db.session.commit()
        return organization


class Storing(PaginatedAPIMixin, db.Model):
    __tablename__ = 'storing'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'))
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)


class TrackingStatus(PaginatedAPIMixin, db.Model):
    __tablename__ = 'tracking_status'
    id = db.Column(db.Integer, primary_key=True)
    condition_id = db.Column(db.Integer, db.ForeignKey('condition.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    tracking_device_id = db.Column(db.Integer, db.ForeignKey('tracking_device.id'))
    value = db.Column(db.Float)
    date_recordered = db.Column(db.DateTime)

    @staticmethod
    def get_statuses_by_product_id(product_id, from_date=None):
        if not from_date:
            return list(reversed(TrackingStatus.query.filter_by(product_id=product_id).all()))
        else:
            return list(reversed(TrackingStatus.query.filter_by(product_id=product_id)
                                 .filter(TrackingStatus.date_recordered > from_date).all()))

    @staticmethod
    def add_status(data):
        product = Product.get_product_by_tracking_device(data['tracking_device_id'])
        if not product:
            return None
        status = TrackingStatus()
        status.value = data['value']
        status.condition_id = data['condition_id']
        status.product_id = product.id
        status.tracking_device_id = data['tracking_device_id']
        status.date_recordered = datetime_parse(data['date_recordered'])

        if product.status not in FAIL_STATUSES:
            condition = Condition.get_condition(status.condition_id)
            if condition.max_value and status.value > condition.max_value or \
                condition.min_value and status.value < condition.min_value:
                product.status = STATUS_SPOILED

        db.session.add(status)
        db.session.commit()
        return status

    def serialize(self):
        return {
            'id': self.id,
            'condition_id': self.condition_id,
            'product_id': self.product_id,
            'tracking_device_id': self.tracking_device_id,
            'value': self.value,
            'date_recordered': str(self.date_recordered)
        }


class TrackingDevice(PaginatedAPIMixin, db.Model):
    __tablename__ = 'tracking_device'
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(120))
    token = db.Column(db.String(120), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)

    @staticmethod
    def get_device(key):
        return TrackingDevice.query.filter_by(key=key).first()

    @staticmethod
    def add_device(data):
        device = TrackingDevice()
        device.key = data['key']
        device.set_password(data['password'])
        db.session.add(device)
        db.session.commit()

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_token(self, expires_in=3600000):
        now = datetime.utcnow()
        if self.token and self.token_expiration and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.commit()
        return self.token

    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

    @staticmethod
    def check_token(token):
        device = TrackingDevice.query.filter_by(token=token).first()
        if device is None or device.token_expiration < datetime.utcnow():
            return None
        return device


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

    def assign_tracking_device(self, tracking_device_id):
        previous_product = Product.get_product_by_tracking_device(tracking_device_id)
        if previous_product:
            previous_product.tracking_device_id = None
        self.tracking_device_id = tracking_device_id
        db.session.commit()

    @staticmethod
    def get_products():
        return list(reversed(Product.query.all()))

    @staticmethod
    def get_product(product_id):
        return Product.query.filter_by(id=product_id).first()

    @staticmethod
    def get_products_by_organization(organization_id):
        return list(reversed(Product.query.filter_by(organization_id=organization_id).all()))

    @staticmethod
    def get_products_by_product_type(product_type_id):
        return list(reversed(Product.query.filter_by(product_type_id=product_type_id).all()))

    @staticmethod
    def get_product_by_tracking_device(tracking_device_id):
        return Product.query.filter_by(tracking_device_id=tracking_device_id).first()

    @staticmethod
    def add_product(data):
        product = Product()
        product.status = STATUS_NEW
        product.name = data['name']
        product.organization_id = data['organization_id']
        product.product_type_id = data['product_type_id']
        product.date_created = datetime.utcnow()
        db.session.add(product)
        db.session.commit()
        return product

    def check_expiration(self):
        if self.status not in FAIL_STATUSES:
            expiration_hours = ProductType.get_product_type(self.product_type_id).expiration_date_length_hours
            if not self.date_created or not expiration_hours:
                return
            expire_date = self.date_created + timedelta(hours=expiration_hours)

            if expire_date <= datetime.utcnow():
                self.status = STATUS_EXPIRED
        db.session.commit()

    def serialize(self, detailed=False, include_statuses=False):
        self.check_expiration()

        res = {
            'id': self.id,
            'name': self.name,
            'organization_id': self.organization_id,
            'tracking_device_id': self.tracking_device_id,
            'product_type_id': self.product_type_id,
            'status_en': self.status,
            'status': _l(self.status),
            'date_created': str(self.date_created)
        }
        if detailed:
            res['organization_name'] = Organization.get_organization(self.organization_id).name
            res['product_type_name'] = ProductType.get_product_type(self.product_type_id).name

        if include_statuses:
            res['tracking_statuses'] = [s.serialize() for s in TrackingStatus.get_statuses_by_product_id(self.id)]
            res['conditions'] = [c.serialize() for c in Condition.get_conditions(self.product_type_id)]
        return res

    def get_statuses(self, from_date):
        self.check_expiration()

        res = {
            'id': self.id,
            'status_en': self.status,
            'status': _l(self.status),
            'tracking_statuses': [s.serialize() for s in TrackingStatus.get_statuses_by_product_id(self.id, from_date=from_date)],
            'conditions': [c.serialize() for c in Condition.get_conditions(self.product_type_id)]
        }
        return res


class Condition(PaginatedAPIMixin, db.Model):
    __tablename__ = 'condition'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    description = db.Column(db.String(120))
    min_value = db.Column(db.Float)
    max_value = db.Column(db.Float)
    product_type_id = db.Column(db.Integer, db.ForeignKey('product_types.id'))

    @staticmethod
    def get_condition(condition_id):
        return Condition.query.filter_by(id=condition_id).first()

    @staticmethod
    def get_conditions(product_type_id):
        return list(reversed(Condition.query.filter_by(product_type_id=product_type_id).all()))

    @staticmethod
    def add_conditions(data):
        condition = Condition()
        condition.name = data['name']
        condition.description = data['description']
        condition.product_type_id = data['product_type_id']
        condition.min_value = data['min_value']
        condition.max_value = data['max_value']
        db.session.add(condition)
        db.session.commit()
        return condition

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'min_value': str(self.min_value) if self.min_value is not None else '',
            'max_value': str(self.max_value) if self.max_value is not None else '',
            'product_type_id': self.product_type_id
        }


class ProductType(PaginatedAPIMixin, db.Model):
    __tablename__ = 'product_types'
    id = db.Column(db.Integer, primary_key=True)
    organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'))
    name = db.Column(db.String(120))
    description = db.Column(db.String(300))
    conditions = db.relationship('Condition', lazy='dynamic')
    image_url = db.Column(db.String(120))
    expiration_date_length_hours = db.Column(db.Integer)

    @staticmethod
    def get_product_type(product_type_id):
        return ProductType.query.filter_by(id=product_type_id).first()

    @staticmethod
    def get_product_types():
        return list(reversed(ProductType.query.all()))

    @staticmethod
    def get_organization_product_types(organization_id):
        return list(reversed(ProductType.query.filter_by(organization_id=organization_id).all()))

    @staticmethod
    def add_product_type(data):
        product_type = ProductType()
        product_type.organization_id = data['organization_id']
        product_type.name = data['name']
        product_type.description = data['description']
        product_type.image_url = data['image_url']
        product_type.expiration_date_length_hours = data['expiration_date_length_hours']
        db.session.add(product_type)
        db.session.commit()
        return product_type

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'expiration_date_length_hours': self.expiration_date_length_hours,
            'description': self.description,
            'image_url': self.image_url,
            'organization_id': self.organization_id
        }
