from app import db
from app.models.base import *
from app.translate import translate as _l
import app.logic.organization
import app.logic.product_type
import app.logic.tracking_status
import app.logic.condition
from datetime import datetime, timedelta
from app.models import product


class Product(product.Product):
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
            expiration_hours = app.logic.product_type.ProductType.get_product_type(self.product_type_id).expiration_date_length_hours
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
            res['organization_name'] = app.logic.organization.Organization.get_organization(self.organization_id).name
            res['product_type_name'] = app.logic.product_type.ProductType.get_product_type(self.product_type_id).name

        if include_statuses:
            res['tracking_statuses'] = [s.serialize() for s in app.logic.tracking_status.TrackingStatus.get_statuses_by_product_id(self.id)]
            res['conditions'] = [c.serialize() for c in app.logic.condition.Condition.get_conditions(self.product_type_id)]
        return res

    def get_statuses(self, from_date):
        self.check_expiration()

        res = {
            'id': self.id,
            'status_en': self.status,
            'status': _l(self.status),
            'tracking_statuses': [s.serialize() for s in
                                  app.logic.tracking_status.TrackingStatus.get_statuses_by_product_id(self.id, from_date=from_date)],
            'conditions': [c.serialize() for c in app.logic.condition.Condition.get_conditions(self.product_type_id)]
        }
        return res
