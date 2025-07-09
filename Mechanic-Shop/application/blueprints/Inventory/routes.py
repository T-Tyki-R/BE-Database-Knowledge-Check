from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from application.models import Inventory, db
from .inventorySchema import inventory_schema
from . import inventory_bp
from application.Utils.util import encode_token, token_required

# Create Endpoints for CRUD operations
# Inventory Endpoints
# GET all inventory parts
# POST a NEW inventory part
# PUT to UPDATE a an inventory part
# DELETE an inventory part

# GET All Part
@inventory_bp.route('/', methods=['GET'])
def get_part():
    parts = db.session.query(Inventory).all()
    return jsonify(inventory_schema.dump(parts, many=True)), 200

# POST a NEW Parts
@inventory_bp.route('/create', methods=['POST'])
def create_part():
    try:
        new_part = inventory_schema.load(request.json)
        db.session.add(new_part)
        db.session.commit()
        return jsonify({
            "message": "Part created successfully",
            "part": inventory_schema.dump(new_part)
        }), 201
    except ValidationError as e:
        return jsonify({"message": "Invalid input", "errors": e.messages}), 400

# PUT to UPDATE an Inventory Part
@inventory_bp.route('/<int:inventory_id>', methods=['PUT'])

def update_part(inventory_id):
    part = db.session.get(Inventory, inventory_id)
    if part:
        try:
            name = request.json.get('name')
            price = request.json.get('price')
            part.name = name
            part.price = price
            db.session.commit()
            return jsonify({
                "message": f"part #{inventory_id} was updated successfully",
                "inventory": inventory_schema.dump(part)
            }), 200
        except ValidationError as e:
            return jsonify({"message": "Invalid input", "errors": e.messages}), 400
    else:
        return jsonify({"message": "inventory not found"}), 404

# DELETE a Inventory Part
@inventory_bp.route('/<int:inventory_id>', methods=['DELETE'])
def delete_parts(inventory_id):
    query = select(Inventory).where(Inventory.inventory_id == inventory_id)
    part = db.session.execute(query).scalars().first()
    
    db.session.delete(part)
    db.session.commit()

    return jsonify({"message": f"Part ID #{inventory_id} was successfully deleted"}), 200
    
# This will be for inventory
@inventory_bp.route("/search", methods=['GET'])
def search_mechanic():
    part = request.args.get("part")

    # use the wirldcard format to allow partial input and display multiple 
    query = select(Inventory).where(Inventory.part.like(f"%{part}%"))
    parts = db.session.execute(query).scalars().all()

    return jsonify(inventory_schema.dump(parts, many=True)), 200
