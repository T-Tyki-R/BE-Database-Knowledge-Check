# Imports
from application import create_app
from application.models import db

app = create_app('DevelopmentConfig')

with app.app_context():
    db.drop_all()  # Drop all tables if they exist
    db.create_all()

# Run the Flask app
app.run()