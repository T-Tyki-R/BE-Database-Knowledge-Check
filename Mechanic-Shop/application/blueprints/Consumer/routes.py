# Imports
from flask import request, jsonify
from marshmallow import ValidationError
from application.models import Consumer, db
from .consumerSchema import consumer_schema
from . import consumer_bp

# Create Endpoints for CRUD operations
# Consumer Endpoints
# GET all Consumers
# GET SPECIFIC Consumer by ID
# POST a NEW Consumer
# PUT to UPDATE a Consumer
# DELETE a Consumer

# GET all Consumers
@consumer_bp.route('/consumers', methods=['GET'])
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
def create_consumer():
    try:
        name = request.json.get('name')
        email = request.json.get('email')
        phone = request.json.get('phone')
        new_consumer = Consumer(name=name, email=email, phone=phone)
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