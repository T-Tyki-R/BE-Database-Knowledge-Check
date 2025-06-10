# Imports
from application.extensions import ma
from application.models import ServiceTicket

class ServiceTicketSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ServiceTicket
        load_instance = True

service_ticket_schema = ServiceTicketSchema()