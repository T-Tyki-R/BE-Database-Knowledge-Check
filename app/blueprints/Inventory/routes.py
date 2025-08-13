from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from app.models import Inventory, db
from .inventorySchema import inventory_schema
from . import inventory_bp

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

        data = request.get_json()

        if not data.get('name'):
            return jsonify({"name": "Missing field: Name"}), 400
        if not data.get('price'):
            return jsonify({"price": "Missing field: Price"}), 400

        
        new_part = Inventory(
            name = data['name'],
            price = data['price']
        )

        db.session.add(new_part)
        db.session.commit()

        return jsonify({
            "message": "part created successfully",
            "part_id": new_part.inventory_id,
            "name": new_part.name,
            "price": new_part.price
        }), 201
        
    except KeyError as e:
        return jsonify({"error": f"Missing required field: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": "An error occurred while creating part"}), 500

# PUT to UPDATE an Inventory Part
@inventory_bp.route('/update/<int:inventory_id>', methods=['PUT'])
def update_part(inventory_id):
    try:
        inventory = db.session.get(Inventory, inventory_id)
        
        if not inventory:
            return jsonify({"message": "part not found"}), 404
        
        data = request.get_json()
        
        # Update fields if provided (no empty validation for updates)
        if 'name' in data:
            inventory.name = data['name']
        if 'price' in data:
            inventory.price = data['price']
        
        db.session.commit()
        
        return jsonify({
            "message": "inventory updated successfully",
            "inventory_id": inventory.inventory_id,
            "name": inventory.name,
            "price": inventory.price,
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# DELETE a Inventory Part
@inventory_bp.route('/delete/<int:inventory_id>', methods=['DELETE'])
def delete_parts(inventory_id):
    query = select(Inventory).where(Inventory.inventory_id == inventory_id)
    part = db.session.execute(query).scalars().first()
    
    db.session.delete(part)
    db.session.commit()

    return jsonify({"message": f"Part ID #{inventory_id} was successfully deleted"}), 200
    

@inventory_bp.route("/search", methods=['GET'])
def search_parts():
    part = request.args.get("name")

    # use the wirldcard format to allow partial input and display multiple 
    query = select(Inventory).where(Inventory.name.like(f"%{part}%"))
    parts = db.session.execute(query).scalars().all()

    return jsonify(inventory_schema.dump(parts, many=True)), 200
