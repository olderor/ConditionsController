from app import db
from app.models import condition


class Condition(condition.Condition):
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
