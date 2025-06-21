# Imports
from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from application.models import Consumer, db
from application.extensions import limiter, cache
from .consumerSchema import consumer_schema, logins_schema
from . import consumer_bp
from application.Utils.util import encode_token

# Create Endpoints for CRUD operations
# Consumer Endpoints
# GET all Consumers
# GET SPECIFIC Consumer by ID
# POST a NEW Consumer
# PUT to UPDATE a Consumer
# DELETE a Consumer

# Create @Token_Required wrapper that''' validate the token and retrun the consumer_id




# GET all Consumers
@consumer_bp.route('/consumers', methods=['GET'])
@cache.cached(timeout=60)  # Cache the response for 60 seconds
def get_consumers():
    consumers = db.session.query(Consumer).all()
    return jsonify(consumer_schema.dump(consumers, many=True)), 200

# GET SPECIFIC Consumer by ID
@consumer_bp.route('/consumers/<int:consumer_id>', methods=['GET'])
def get_consumer(consumer_id):
    consumer = db.session.get(Consumer, consumer_id)
    if consumer:
        return jsonify({
            "message": "Consumer found",
            "consumer": consumer_schema.dump(consumer)
        }), 200
    else:
        return jsonify({"message": "Consumer not found"}), 404

# POST a NEW Consumer
@consumer_bp.route('/consumers', methods=['POST'])
@limiter.limit("5 per minute")  # Rate limit to 5 requests per minute
def create_consumer():
    try:
        name = request.json.get('name')
        email = request.json.get('email')
        phone = request.json.get('phone')
        password = request.json.get('password')
        new_consumer = Consumer(name=name, email=email, phone=phone, password=password)
        db.session.add(new_consumer)
        db.session.commit()
        return jsonify({
            "message": "Consumer created successfully",
            "consumer": consumer_schema.dump(new_consumer)
        }), 201
    except ValidationError as e:
        return jsonify({"message": "Invalid input", "errors": e.messages}), 400

# PUT to UPDATE a Consumer
@consumer_bp.route('/consumers/<int:consumer_id>', methods=['PUT'])
def update_consumer(consumer_id):
    consumer = db.session.get(Consumer, consumer_id)
    if consumer:
        try:
            name = request.json.get('name')
            email = request.json.get('email')
            phone = request.json.get('phone')
            consumer.name = name
            consumer.email = email
            consumer.phone = phone
            db.session.commit()
            return jsonify({
                "message": f"Consumer #{consumer_id} was updated successfully",
                "consumer": consumer_schema.dump(consumer)
            }), 200
        except ValidationError as e:
            return jsonify({"message": "Invalid input", "errors": e.messages}), 400
    else:
        return jsonify({"message": "Consumer not found"}), 404

# DELETE a Consumer
@consumer_bp.route('/consumers/<int:consumer_id>', methods=['DELETE'])
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
        return jsonify({"message": "Invalid email or password"}), 401