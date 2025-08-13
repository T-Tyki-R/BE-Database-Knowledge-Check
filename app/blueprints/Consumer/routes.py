# Imports
from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from app.models import Consumer, db
from app.extensions import limiter, cache
from .consumerSchema import consumer_schema, logins_schema
from . import consumer_bp
from app.Utils.util import encode_token, token_required

# Create Endpoints for CRUD operations
# Consumer Endpoints
# GET all Consumers
# POST a NEW Consumer
# PUT to UPDATE a Consumer
# DELETE a Consumer

# GET all Consumers
@consumer_bp.route('/', methods=['GET'])
@cache.cached(timeout=60)  # Cache the response for 60 seconds
def get_consumers():
    consumers = db.session.query(Consumer).all()
    return jsonify(consumer_schema.dump(consumers, many=True)), 200

# POST a NEW Consumer
@consumer_bp.route('/create', methods=['POST'])
@limiter.limit("5 per minute")  # Rate limit to 5 requests per minute
def create_consumer():
    try:

        data = request.get_json()

        if not data.get('name'):
            return jsonify({"name": "Missing field: Name"}), 400
        if not data.get('email'):
            return jsonify({"email": "Missing field: Email"}), 400
        if not data.get('phone'):
            return jsonify({"phone": "Missing field: Phone"}), 400
        if not data.get('password'):
            return jsonify({"password": "Missing field: Password"}), 400
        
        new_consumer = Consumer(
            name = data['name'],
            email = data['email'],
            phone = data['phone'],
            password = data['password']
        )

        db.session.add(new_consumer)
        db.session.commit()

        return jsonify({
            "message": "Consumer created successfully",
            "consumer_id": new_consumer.consumer_id,
            "name": new_consumer.name,
            "email": new_consumer.email,
            "phone": new_consumer.phone
        }), 201
        
    except KeyError as e:
        return jsonify({"error": f"Missing required field: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": "An error occurred while creating consumer"}), 500

# PUT to UPDATE a Consumer
@consumer_bp.route('/update', methods=['PUT'])
@token_required
def update_consumer(consumer_id):  # consumer_id comes from token_required decorator
    try:
        consumer = db.session.get(Consumer, consumer_id)
        
        if not consumer:
            return jsonify({"message": "Consumer not found"}), 404
        
        data = request.get_json()
        
        # Update fields if provided (no empty validation for updates)
        if 'name' in data:
            consumer.name = data['name']
        if 'email' in data:
            consumer.email = data['email']
        if 'phone' in data:
            consumer.phone = data['phone']
        if 'password' in data:
            consumer.password = data['password']
        
        db.session.commit()
        
        return jsonify({
            "message": "Consumer updated successfully",
            "consumer_id": consumer.consumer_id,
            "name": consumer.name,
            "email": consumer.email,
            "phone": consumer.phone
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# DELETE a Consumer
@consumer_bp.route('/delete', methods=['DELETE'])
@token_required
def delete_consumer(consumer_id):
    consumer = db.session.get(Consumer, consumer_id)
    if consumer:
        try:
            db.session.delete(consumer)
            db.session.commit()
            return jsonify({"message": f"Consumer #{consumer_id} was successfully deleted"}), 200
        except ValidationError as e:
            return jsonify(e.messages), 400
    else:
        return jsonify({"message": "Consumer not found"}), 404
    
# POST Login Endpoint
@consumer_bp.route("/login", methods=['POST'])
def login():
    try:
        # Create credentials
        creditials = logins_schema.load(request.json)
        email = creditials.email
        password = creditials.password

    except ValidationError as e:
        return jsonify(e.messages), 400   
    
    query = select(Consumer).where(
        Consumer.email == email,
        Consumer.password == password
    )
    consumer = db.session.execute(query).scalars().first()

    if consumer:
        # Generate JWT token
        token = encode_token(consumer.consumer_id)
        response = {
            "status": "success",
            "message": "Login successful",
            "token": token
        }
        return jsonify(response), 200
    else:
        return jsonify({"message": "Invalid email or password"}), 400