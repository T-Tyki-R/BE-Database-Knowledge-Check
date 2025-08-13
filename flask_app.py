# Imports
from app import create_app
from app.models import db

app = create_app('ProductionConfig')

with app.app_context():
    # db.drop_all()  # Drop all tables if they exist (Optional)
    db.create_all()



