# Imports
from flask import Flask
from .extensions import ma, limiter, cache
from .models import db
from .blueprints.Consumer import consumer_bp
from .blueprints.Mechanic import mechanic_bp
from .blueprints.Service_Tickets import service_ticket_bp
from .blueprints.Inventory import inventory_bp

def create_app(config_name):
    # Create Flask application instance
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(f"config.{config_name}")

    # Initialize Extensions
    ma.init_app(app)

    # Initialize SQLAlchemy
    db.init_app(app)

    # Initialize Limiter
    limiter.init_app(app)

    # Initialize Cache
    cache.init_app(app)

    # Register Blueprints
    app.register_blueprint(consumer_bp, url_prefix='/consumers')
    app.register_blueprint(mechanic_bp, url_prefix='/mechanics')
    app.register_blueprint(service_ticket_bp, url_prefix='/service-tickets')
    app.register_blueprint(inventory_bp, url_prefix='/inventory')

    return app