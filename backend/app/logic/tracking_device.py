import base64
import os
from datetime import datetime, timedelta
from app import db
from app.models import tracking_device
from werkzeug.security import generate_password_hash, check_password_hash


class TrackingDevice(tracking_device.TrackingDevice):
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
