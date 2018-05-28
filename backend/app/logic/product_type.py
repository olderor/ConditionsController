from app import db
from app.models import product_type


class ProductType(product_type.ProductType):
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
