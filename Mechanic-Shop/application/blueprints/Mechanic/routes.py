# Imports
from flask import request, jsonify
from marshmallow import ValidationError
from application.models import Mechanic, db
from .mechanicSchema import mechanic_schema
from . import mechanic_bp

# Create Endpoints for CRUD operations
# Mechanic Endpoints
# GET all Mechanics
# GET SPECIFIC Mechanic by ID
# POST a NEW Mechanic
# PUT to UPDATE a Mechanic
# DELETE a Mechanic

# GET all Mechanics
@mechanic_bp.route('/mechanics', methods=['GET'])
def get_Mechanics():
    mechanic = db.session.query(Mechanic).all()
    return jsonify(mechanic_schema.dump(mechanic, many=True)), 200

# GET SPECIFIC Mechanic by ID
@mechanic_bp.route('/mechanics/<int:mechanic_id>', methods=['GET'])
def get_Mechanic(mechanic_id):
    mechanic = db.session.get(Mechanic, mechanic_id)
    if mechanic:
        return jsonify({
            "message": "Mechanic found",
            "Mechanic": mechanic_schema.dump(mechanic)
        }), 200
    else:
        return jsonify({"message": "Mechanic not found"}), 404

# POST a NEW Mechanic
@mechanic_bp.route('/mechanics', methods=['POST'])
def create_Mechanic():
    try:
        name = request.json.get('name')
        email = request.json.get('email')
        phone = request.json.get('phone')
        salary = request.json.get('salary', 0.00)  # Default salary to 0 if not provided
        new_mechanic = Mechanic(name=name, email=email, phone=phone, salary=salary)
        db.session.add(new_mechanic)
        db.session.commit()
        return jsonify({
            "message": "Mechanic created successfully",
            "Mechanic": mechanic_schema.dump(new_mechanic)
        }), 201
    except ValidationError as e:
        return jsonify({"message": "Invalid input", "errors": e.messages}), 400

# PUT to UPDATE a Mechanic
@mechanic_bp.route('/mechanics/<int:mechanic_id>', methods=['PUT'])
def update_Mechanic(mechanic_id):
    mechanic = db.session.get(Mechanic, mechanic_id)
    if mechanic:
        try:
            name = request.json.get('name')
            email = request.json.get('email')
            phone = request.json.get('phone')
            salary = request.json.get('salary', mechanic.salary)  # Use existing salary if not provided
            mechanic.name = name
            mechanic.email = email
            mechanic.phone = phone
            mechanic.salary = salary
            db.session.commit()
            return jsonify({
                "message": f"Mechanic #{mechanic_id} was updated successfully",
                "Mechanic": mechanic_schema.dump(mechanic)
            }), 200
        except ValidationError as e:
            return jsonify({"message": "Invalid input", "errors": e.messages}), 400
    else:
        return jsonify({"message": "Mechanic not found"}), 404

# DELETE a Mechanic
@mechanic_bp.route('/mechanics/<int:mechanic_id>', methods=['DELETE'])
def delete_Mechanic(mechanic_id):
    mechanic = db.session.get(Mechanic, mechanic_id)
    if mechanic:
        try:
            db.session.delete(mechanic)
            db.session.commit()
            return jsonify({"message": f"Mechanic #{mechanic_id} was successfully deleted"}), 200
        except ValidationError as e:
            return jsonify(e.messages), 400
    else:
        return jsonify({"message": "Mechanic not found"}), 404