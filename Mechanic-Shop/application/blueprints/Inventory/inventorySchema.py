# Imports
from application.extensions import ma
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from application.models import Inventory

class InventorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Inventory
        load_instance = True

inventory_schema = InventorySchema()