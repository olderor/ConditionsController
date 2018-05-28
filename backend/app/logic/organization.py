from app import db
from app.models import organization


class Organization(organization.Organization):
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
