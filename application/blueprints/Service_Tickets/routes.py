# Imports
from flask import request, jsonify
from sqlalchemy import select
from marshmallow import ValidationError
from application.models import ServiceTicket, db, Mechanic, Inventory
from .serviceTicketSchema import service_tickets_schema, return_service_ticket_schema, edit_ticket_schema, create_service_ticket_schema
from . import service_ticket_bp

# Create Endpoints for CRUD operations
# Service Ticket Endpoints
# GET all Service Tickets
# GET SPECIFIC Service Ticket by ID
# POST a NEW Service Ticket
# PUT to UPDATE a Service Ticket
# DELETE a Service Ticket

# GET all service_tickets
@service_ticket_bp.route('/', methods=['GET'])
def get_service_tickets():
    tickets = select(ServiceTicket)
    res = db.session.execute(tickets).scalars().all()
    return service_tickets_schema.jsonify(res), 200

# POST a NEW service_ticket
@service_ticket_bp.route('/create', methods=['POST'])
def create_service_ticket():
    #check to see if consumer_id exists, if not, throw error
    print("Schema fields:", list(create_service_ticket_schema.fields.keys()))
    try:
        ticket_data = create_service_ticket_schema.load(request.json)
    except ValidationError as e:
        return jsonify({"message": "Invalid input", "errors": e.messages}), 400
    
    new_ticket = ServiceTicket(service_date= ticket_data['service_date'],
                               consumer_id= ticket_data['consumer_id'],
                               vin= ticket_data['vin'],
                               description= ticket_data['description'])
    
    for mechanic_id in ticket_data["mechanics"]:
        query = select(Mechanic).where(Mechanic.mechanic_id == mechanic_id)
        mechanic = db.session.execute(query).scalar()
        if mechanic:
            new_ticket.mechanics.append(mechanic)
        else:
            return jsonify({"message": "Invalid Mechanic ID..."}), 400
    for inventory_id in ticket_data["parts"]:
        query = select(Inventory).where(Inventory.inventory_id == inventory_id)
        part = db.session.execute(query).scalar()
        if part:
            new_ticket.parts.append(part)
        else:
            return jsonify({"message": "Invalid Part ID..."}), 400
    
    db.session.add(new_ticket)
    db.session.commit()

    return return_service_ticket_schema.jsonify(new_ticket), 201

# DELETE a service_ticket
@service_ticket_bp.route('/delete/<int:service_ticket_id>', methods=['DELETE'])
def delete_service_ticket(service_ticket_id):
    service_ticket = select(ServiceTicket).where(ServiceTicket.ticket_id == service_ticket_id)
    ticket = db.session.execute(service_ticket).scalars().first()
    
    db.session.delete(ticket)
    db.session.commit()

    return jsonify({"message": f"service_ticket #{service_ticket_id} was successfully deleted"}), 200
    
    
# PUT Edit tickets
@service_ticket_bp.route("/update/<int:service_ticket_id>", methods=['PUT'])
def edit_tickets(service_ticket_id):
    try: 
       ticket_edit = edit_ticket_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    query = select(ServiceTicket).where(ServiceTicket.ticket_id == service_ticket_id)
    ticket = db.session.execute(query).scalars().first()

    for mechanic_id in ticket_edit['add_mechanic_ids']:
        query = select(Mechanic).where(Mechanic.mechanic_id == mechanic_id)
        mechanic = db.session.execute(query).scalars().first()

        if mechanic and mechanic not in ticket.mechanics:
            ticket.mechanics.append(mechanic)

    for mechanic_id in ticket_edit['remove_mechanic_ids']:
        query = select(Mechanic).where(Mechanic.mechanic_id == mechanic_id)
        mechanic = db.session.execute(query).scalars().first()

        if mechanic and mechanic in ticket.mechanics:
            ticket.mechanics.remove(mechanic) 

    # Add parts
    for inventory_id in ticket_edit['add_part_ids']:
        query = select(Inventory).where(Inventory.inventory_id == inventory_id)
        part = db.session.execute(query).scalars().first()
        if part and part not in ticket.parts:
            ticket.parts.append(part)

    # Remove parts
    for inventory_id in ticket_edit['remove_part_ids']:
        query = select(Inventory).where(Inventory.inventory_id == inventory_id)
        part = db.session.execute(query).scalars().first()
        if part and part in ticket.parts:
            ticket.parts.remove(part)

    db.session.commit()
    return return_service_ticket_schema.jsonify(ticket)