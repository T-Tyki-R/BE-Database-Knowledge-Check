# Imports
from flask import request, jsonify
from marshmallow import ValidationError
from application.models import ServiceTicket, db
from .serviceTicketSchema import service_ticket_schema
from . import service_ticket_bp

# Create Endpoints for CRUD operations
# Service Ticket Endpoints
# GET all Service Tickets
# GET SPECIFIC Service Ticket by ID
# POST a NEW Service Ticket
# PUT to UPDATE a Service Ticket
# DELETE a Service Ticket

# GET all service_tickets
@service_ticket_bp.route('/service_tickets', methods=['GET'])
def get_service_tickets():
    ticket = db.session.query(ServiceTicket).all()
    return jsonify(service_ticket_schema.dump(ticket, many=True)), 200

# GET SPECIFIC service_ticket by ID
@service_ticket_bp.route('/service_tickets/<int:service_ticket_id>', methods=['GET'])
def get_service_ticket(service_ticket_id):
    service_ticket = db.session.get(ServiceTicket, service_ticket_id)
    if service_ticket:
        return jsonify({
            "message": "Service ticket found",
            "service_ticket": service_ticket_schema.dump(service_ticket)
        }), 200
    else:
        return jsonify({"message": "Service ticket not found"}), 404

# POST a NEW service_ticket
@service_ticket_bp.route('/service_tickets', methods=['POST'])
def create_service_ticket():
    #check to see if consumer_id exists, if not, throw error
    try:
        consumer_id = request.json.get('consumer_id')
        if not consumer_id:
            return jsonify({"message": "consumer_id is required"}), 400
        vin = request.json.get('vin')
        service_date = request.json.get('service_date')
        description = request.json.get('description')
        new_service_ticket = ServiceTicket(
            consumer_id=consumer_id,
            vin=vin,
            service_date=service_date,
            description=description
        )
        db.session.add(new_service_ticket)
        db.session.commit()
        return jsonify({
            "message": "Service ticket created successfully",
            "service_ticket": service_ticket_schema.dump(new_service_ticket)
        }), 201
    except ValidationError as e:
        return jsonify({"message": "Invalid input", "errors": e.messages}), 400

# PUT to UPDATE a service_ticket
@service_ticket_bp.route('/service_tickets/<int:service_ticket_id>', methods=['PUT'])
def update_service_ticket(service_ticket_id):
    service_ticket = db.session.get(ServiceTicket, service_ticket_id)
    if service_ticket:
        try:
            consumer_id = request.json.get('consumer_id')
            vin = request.json.get('vin')
            service_date = request.json.get('service_date')
            description = request.json.get('description')
            service_ticket.consumer_id = consumer_id
            service_ticket.vin = vin
            service_ticket.service_date = service_date
            service_ticket.description = description
            db.session.commit()
            return jsonify({
                "message": f"service_ticket #{service_ticket_id} was updated successfully",
                "service_ticket": service_ticket_schema.dump(service_ticket)
            }), 200
        except ValidationError as e:
            return jsonify({"message": "Invalid input", "errors": e.messages}), 400
    else:
        return jsonify({"message": "service_ticket not found"}), 404

# DELETE a service_ticket
@service_ticket_bp.route('/service_tickets/<int:service_ticket_id>', methods=['DELETE'])
def delete_service_ticket(service_ticket_id):
    service_ticket = db.session.get(ServiceTicket, service_ticket_id)
    if service_ticket:
        try:
            db.session.delete(service_ticket)
            db.session.commit()
            return jsonify({"message": f"service_ticket #{service_ticket_id} was successfully deleted"}), 200
        except ValidationError as e:
            return jsonify(e.messages), 400
    else:
        return jsonify({"message": "service_ticket not found"}), 404