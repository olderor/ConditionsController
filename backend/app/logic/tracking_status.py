from app import db
from app.models.base import *
from app.models import tracking_status
import app.logic.product
import app.logic.condition
from dateutil.parser import parse as datetime_parse


class TrackingStatus(tracking_status.TrackingStatus):
    @staticmethod
    def get_statuses_by_product_id(product_id, from_date=None):
        if not from_date:
            return list(reversed(TrackingStatus.query.filter_by(product_id=product_id).all()))
        else:
            return list(reversed(TrackingStatus.query.filter_by(product_id=product_id)
                                 .filter(TrackingStatus.date_recordered > from_date).all()))

    @staticmethod
    def add_status(data):
        product = app.logic.product.Product.get_product_by_tracking_device(data['tracking_device_id'])
        if not product:
            return None
        status = TrackingStatus()
        status.value = data['value']
        status.condition_id = data['condition_id']
        status.product_id = product.id
        status.tracking_device_id = data['tracking_device_id']
        status.date_recordered = datetime_parse(data['date_recordered'])

        if product.status not in FAIL_STATUSES:
            condition = app.logic.condition.Condition.get_condition(status.condition_id)
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
