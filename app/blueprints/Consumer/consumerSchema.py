# Imports
from app.extensions import ma
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.models import Consumer

class ConsumerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Consumer
        load_instance = True

consumer_schema = ConsumerSchema()
logins_schema = ConsumerSchema(exclude=('name', 'phone'))  # Exclude sensitive fields for login