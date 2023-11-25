from app_factory import db


class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, name="unique_email_constraint")
    username = db.Column(db.String(20), unique=False, nullable=False)
    password = db.Column(db.String(60), nullable=True)
    age = db.Column(db.Integer)
    address = db.Column(db.String(100))
    contact_number = db.Column(db.String(20))
    email_address = db.Column(db.String(100))
    reason_to_qualify = db.Column(db.Text)
    employment_status = db.Column(db.String(20))
    number_of_pets = db.Column(db.Integer)
    animal_id = db.Column(db.Integer, db.ForeignKey('animal.id', name='fk_client_animal_id'))
    animals = db.relationship('ClientAnimal', back_populates='client')
    # Define a relationship with the Volunteer model
    volunteers = db.relationship('Volunteer', back_populates='client')
    image_path = db.Column(db.String(200))  # Adjust the length as needed
