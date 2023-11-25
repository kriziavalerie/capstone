from app_factory import db

class AnimalOwner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    animal_id = db.Column(db.Integer, db.ForeignKey('animal.id'), nullable=False)
    name = db.Column(db.String(30))
    address = db.Column(db.String(100))
    contact_number = db.Column(db.String(20))
    email_address = db.Column(db.String(30))
    age = db.Column(db.Integer)
    date_applied = db.Column(db.Date)
    date_adopted = db.Column(db.Date)
