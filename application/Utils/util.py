# Imports
from datetime import datetime, timedelta, timezone
from jose import jwt
import jose
from functools import wraps
from flask import request, jsonify

# Create Secret Key
SECRET_KEY = "super-duper-secret"

def encode_token(consumer_id):
    payload = {
        'exp': datetime.now(timezone.utc) + timedelta(days = 0, hours= 2),  # Token valid for 1 day
        'iat': datetime.now(timezone.utc),  # Issued at time
        'sub': str(consumer_id ) 
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

# Create a decorator to require token for certain routes
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split()[1]
            if not token:
                return jsonify({"message" : "missing token"}), 400
            
            try:
                data = jwt.decode(token, SECRET_KEY, algorithms='HS256')
                print(data)
                consumer_id = data["sub"]
            except jwt.ExpiredSignatureError as e:
                return jsonify({"message" : "token expired"}), 400
            except jose.exceptions.JWTError:
                return jsonify({"message" : "invalid token"}), 400
            
            return f(consumer_id, *args, **kwargs)
        
        else:
            return jsonify({"message" : "You must be logged in to access"}), 400
        
    return decorated



           

