from app_factory import db
from models.Client import Client
from models.Animal import Animal

class ClientAnimal(db.Model):
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), primary_key=True)
    animal_id = db.Column(db.Integer, db.ForeignKey('animal.id'), primary_key=True)
    status = db.Column(db.String(20))  # Pending, Approved, Declined
    date_applied = db.Column(db.Date)
    appointment_date = db.Column(db.Date)
    time_applied = db.Column(db.String(8))


    # Define relationships to access related objects
    client = db.relationship('Client', back_populates='animals')
    animal = db.relationship('Animal', back_populates='clients')

# Add relationships to the Client and Animal models
Client.animals = db.relationship('ClientAnimal', back_populates='client')
Animal.clients = db.relationship('ClientAnimal', back_populates='animal')
