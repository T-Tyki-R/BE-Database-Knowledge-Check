# Imports
from datetime import datetime, timedelta, timezone
from jose import jwt
import jose

# Create Secret Key
SECRET_KEY = "super-duper-secret"

def encode_token(user_id):
    payload = {
        'exp': datetime.now(timezone.utc) + timedelta(days = 0, hours= 2),  # Token valid for 1 day
        'iat': datetime.now(timezone.utc),  # Issued at time
        'sub': str(user_id ) 
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token
