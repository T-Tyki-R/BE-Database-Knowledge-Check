# Imports
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import ForeignKey
from flask_sqlalchemy import SQLAlchemy

# Create Base Class
class Base(DeclarativeBase):
    pass

# Initialize SQLAlchemy
db = SQLAlchemy(model_class=Base)

# Define Table/Model Classes
# Consumer Class
class Consumer(Base):
    __tablename__ = 'consumer'
    consumer_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    email: Mapped[str] = mapped_column(db.String(100), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(db.String(20), nullable=False)
    password: Mapped[str] = mapped_column(db.String(255), nullable=False)

# Mechanic Class
class Mechanic(Base):
    __tablename__ = 'mechanic'
    mechanic_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    email: Mapped[str] = mapped_column(db.String(100), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(db.String(20), nullable=False)
    salary: Mapped[float] = mapped_column(nullable=False)

# Service Ticket Class
class ServiceTicket(Base):
    __tablename__ = 'service_ticket'
    ticket_id: Mapped[int] = mapped_column(primary_key=True)
    consumer_id: Mapped[int] = mapped_column(ForeignKey('consumer.consumer_id'))
    vin: Mapped[str] = mapped_column(db.String(17), nullable=False)
    service_date: Mapped[str] = mapped_column(db.String(10), nullable=False)  # Format: YYYY-MM-DD
    description: Mapped[str] = mapped_column(db.String(500), nullable=False)

