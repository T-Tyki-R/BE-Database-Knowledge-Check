# Imports
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import date
from flask_sqlalchemy import SQLAlchemy
from typing import List

# Create Base Class
class Base(DeclarativeBase):
    pass

# Initialize SQLAlchemy
db = SQLAlchemy(model_class=Base)

service_mechanic = db.Table(
   "service_mechanic",
   Base.metadata,
   db.Column("mechanic_id", db.ForeignKey("mechanic.mechanic_id")),
   db.Column("ticket_id", db.ForeignKey("service_ticket.ticket_id"))
)

service_parts = db.Table(
    "service_parts",
    Base.metadata,
    db.Column("inventory_id", db.ForeignKey("inventory.inventory_id")),
    db.Column("ticket_id", db.ForeignKey("service_ticket.ticket_id"))
)

# Service Ticket Class
class ServiceTicket(Base):
    __tablename__ = 'service_ticket'
    ticket_id: Mapped[int] = mapped_column(primary_key=True)
    consumer_id: Mapped[int] = mapped_column(db.ForeignKey("consumer.consumer_id"), nullable=False)
    vin: Mapped[str] = mapped_column(db.String(17), nullable=False)
    service_date: Mapped[date] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(db.String(500), nullable=False)

    consumer: Mapped["Consumer"] = db.relationship(back_populates="service_tickets")
    mechanics: Mapped[List["Mechanic"]] = db.relationship(
        secondary=service_mechanic,
        back_populates="service_tickets" )
    parts:  Mapped[List["Inventory"]] = db.relationship(
        secondary = service_parts,
        back_populates= "service_tickets")


# Consumer Class
class Consumer(Base):
    __tablename__ = "consumer"
    consumer_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    email: Mapped[str] = mapped_column(db.String(100), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(db.String(20), nullable=False)
    password: Mapped[str] = mapped_column(db.String(255), nullable=False)

    service_tickets: Mapped[List["ServiceTicket"]] = db.relationship(back_populates="consumer", cascade="all, delete")

# Mechanic Class
class Mechanic(Base):
    __tablename__ = 'mechanic'
    mechanic_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    email: Mapped[str] = mapped_column(db.String(100), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(db.String(20), nullable=False)
    salary: Mapped[float] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(db.String(255), nullable=False)

    service_tickets: Mapped[List["ServiceTicket"]] = db.relationship(
        secondary=service_mechanic,
        back_populates="mechanics"
                )

class Inventory(Base):
    __tablename__ = 'inventory'
    inventory_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(100), nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)

    service_tickets: Mapped[List["ServiceTicket"]] = db.relationship(
        secondary=service_parts,
        back_populates="parts"
    )

