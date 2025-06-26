# Imports
from application.extensions import ma
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from application.models import Consumer

class ConsumerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Consumer
        load_instance = True

consumer_schema = ConsumerSchema()
logins_schema = ConsumerSchema(exclude=('name', 'phone'))  # Exclude sensitive fields for login