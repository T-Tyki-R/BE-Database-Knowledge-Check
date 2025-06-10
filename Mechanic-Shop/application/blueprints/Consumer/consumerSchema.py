# Imports
from application.extensions import ma
from application.models import Consumer

class ConsumerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Consumer
        load_instance = True

consumer_schema = ConsumerSchema()