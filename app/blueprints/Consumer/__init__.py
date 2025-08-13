# Imports
from flask import Blueprint
 
consumer_bp = Blueprint('consumer_bp', __name__)

from . import routes


