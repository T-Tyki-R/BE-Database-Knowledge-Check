# Imports
from application.extensions import ma
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from application.models import ServiceTicket
from marshmallow import fields

class ServiceTicketSchema(ma.SQLAlchemyAutoSchema):
    mechanics = fields.Nested("MechanicSchema", many=True)
    consumer = fields.Nested("ConsumerSchema")
    class Meta:
        model = ServiceTicket
        include_fk = True 
        # include_relationships = True
        fields = (
            ""
            "ticket_id",
            "consumer_id",
            "vin",
            "service_date",
            "description",
            "mechanics",
            "consumer"
        )

class CreateServiceTicketSchema(ma.Schema):
    consumer_id = fields.Int(required=True)
    vin = fields.Str(required=True)
    service_date = fields.Date(required=True)
    description = fields.Str(required=True)
    mechanics = fields.List(fields.Int(), required=True)
    
    class Meta:
        fields = ("consumer_id", "vin", "service_date", "description", "mechanics")

class EditTicketSchema(ma.Schema):
    add_mechanic_ids = fields.List(fields.Int(), required=True)
    remove_mechanic_ids = fields.List(fields.Int(), required=True)
    class Meta:
        fields = ("add_mechanic_ids", "remove_mechanic_ids")

service_ticket_schema = ServiceTicketSchema()
service_tickets_schema = ServiceTicketSchema(many=True)
return_service_ticket_schema = ServiceTicketSchema(exclude=["consumer_id"])
create_service_ticket_schema = CreateServiceTicketSchema()
edit_ticket_schema = EditTicketSchema()