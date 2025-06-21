# Imports
from flask import request, jsonify
from marshmallow import ValidationError
from application.models import Mechanic, db
from .mechanicSchema import mechanic_schema, logins_schema
from . import mechanic_bp
from sqlalchemy import select
from application.extensions import limiter, cache
from application.Utils.util import encode_token, token_required

# Create Endpoints for CRUD operations
# Mechanic Endpoints
# GET all Mechanics
# GET SPECIFIC Mechanic by ID
# POST a NEW Mechanic
# PUT to UPDATE a Mechanic
# DELETE a Mechanic

# GET all Mechanics
@mechanic_bp.route('/mechanics', methods=['GET'])
@cache.cached(timeout=60)  # Cache the response for 60 seconds
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
@limiter.limit("5 per minute")  # Rate limit to 5 requests per minute
def create_Mechanic():
    try:
        name = request.json.get('name')
        email = request.json.get('email')
        phone = request.json.get('phone')
        salary = request.json.get('salary', 0.00)  # Default salary to 0 if not provided
        password = request.json.get('password')
        new_mechanic = Mechanic(name=name, email=email, phone=phone, salary=salary, password=password)
        db.session.add(new_mechanic)
        db.session.commit()
        return jsonify({
            "message": "Mechanic created successfully",
            "Mechanic": mechanic_schema.dump(new_mechanic)
        }), 201
    except ValidationError as e:
        return jsonify({"message": "Invalid input", "errors": e.messages}), 400

# PUT to UPDATE a Mechanic
@mechanic_bp.route('/', methods=['PUT'])
@token_required
def update_Mechanic(mechanic_id):
    mechanic = db.session.get(Mechanic, mechanic_id)
    if mechanic:
        try:
            name = request.json.get('name')
            email = request.json.get('email')
            phone = request.json.get('phone')
            salary = request.json.get('salary', mechanic.salary)  # Use existing salary if not provided
            password = request.json.get('password')
            mechanic.name = name
            mechanic.email = email
            mechanic.phone = phone
            mechanic.salary = salary
            mechanic.password = password
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
@mechanic_bp.route('/', methods=['DELETE'])
@token_required
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
    
# POST Login Endpoint
@mechanic_bp.route("/login", methods=['POST'])
def login():
    try:
        # Create credentials
        creditials = logins_schema.load(request.json)
        email = creditials.email
        password = creditials.password

    except ValidationError as e:
        return jsonify(e.messages), 400   
    
    query = select(Mechanic).where(
        Mechanic.email == email,
        Mechanic.password == password
    )
    mechanic = db.session.execute(query).scalars().first()

    if Mechanic:
        # Generate JWT token
        token = encode_token(mechanic.mechanic_id)
        response = {
            "status": "success",
            "message": "Login successful",
            "token": token
        }
        return jsonify(response), 200
    else:
        return jsonify({"message": "Invalid email or password"}), 401