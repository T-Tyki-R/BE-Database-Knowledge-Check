# Imports
from application.extensions import ma
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from application.models import Mechanic

class MechanicSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Mechanic
        load_instance = True

class MechanicDisplaySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Mechanic
        load_instance = True
        fields = ("mechanic_id", "name", "email", "phone")  # Only include safe fields

# Schema instances
mechanic_schema = MechanicSchema()
mechanic_display_schema = MechanicDisplaySchema()
mechanics_display_schema = MechanicDisplaySchema(many=True)
logins_schema = MechanicSchema(exclude=('name', 'email', 'phone'))  # Exclude sensitive fields for login