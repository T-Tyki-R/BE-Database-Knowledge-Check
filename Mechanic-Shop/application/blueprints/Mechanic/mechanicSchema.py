# Imports
from application.extensions import ma
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from application.models import Mechanic

class MechanicSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Mechanic
        load_instance = True

mechanic_schema = MechanicSchema()
logins_schema = MechanicSchema(exclude=('name', 'phone', 'salary'))  # Exclude sensitive fields for login