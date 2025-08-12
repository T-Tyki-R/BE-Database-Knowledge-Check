# Imports
from application.extensions import ma
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from application.models import ServiceTicket
from marshmallow import fields

class ServiceTicketSchema(ma.SQLAlchemyAutoSchema):
    mechanics = fields.Nested("MechanicSchema", many=True)
    parts = fields.Nested("InventorySchema", many= True)
    consumer = fields.Nested("ConsumerSchema")
    class Meta:
        model = ServiceTicket
        include_fk = True 
        fields = (
            ""
            "ticket_id",
            "consumer_id",
            "vin",
            "service_date",
            "description",
            "mechanics",
            "consumer",
            "parts"
        )

class CreateServiceTicketSchema(ma.Schema):
    consumer_id = fields.Int(required=True)
    vin = fields.Str(required=True)
    service_date = fields.Date(required=True)
    description = fields.Str(required=True)
    mechanics = fields.List(fields.Int(), required=True)
    parts = fields.List(fields.Int(), required= True)
    
    class Meta:
        fields = ("consumer_id", "vin", "service_date", "description", "mechanics", "parts")

class EditTicketSchema(ma.Schema):
    add_mechanic_ids = fields.List(fields.Int(), required=True)
    remove_mechanic_ids = fields.List(fields.Int(), required=True)
    add_part_ids = fields.List(fields.Int(), required=True)
    remove_part_ids = fields.List(fields.Int(), required=True)
    class Meta:
        fields = ("add_mechanic_ids", "remove_mechanic_ids", "add_part_ids", "remove_part_ids")

service_ticket_schema = ServiceTicketSchema()
service_tickets_schema = ServiceTicketSchema(many=True)
return_service_ticket_schema = ServiceTicketSchema(exclude=["consumer_id"])
create_service_ticket_schema = CreateServiceTicketSchema()
edit_ticket_schema = EditTicketSchema()