# Imports
from application.extensions import ma
from application.models import ServiceTicket
from marshmallow import fields

class ServiceTicketSchema(ma.SQLAlchemyAutoSchema):
    # consumer_id = fields.Int() # Kept getting keyword error. gitCopilot suggested this
    # mechnaic_id = fields.List(fields.Int(), load_only = True, required= True)
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

class EditTicketSchema(ma.Schema):
    add_mechanic_ids = fields.List(fields.Int(), required=True)
    remove_mechanic_ids = fields.List(fields.Int(), required=True)
    class Meta:
        fields = ("add_mechanic_ids", "remove_mechanic_ids")

service_ticket_schema = ServiceTicketSchema()
service_tickets_schema = ServiceTicketSchema(many=True)
return_service_ticket_schema = ServiceTicketSchema(exclude=["consumer_id"])
edit_ticket_schema = EditTicketSchema()