from app_factory import db


class AnimalDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    animal_id = db.Column(db.Integer, db.ForeignKey('animal.id'), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    tag_number = db.Column(db.String(20))
    status = db.Column(db.String(20))
    estimated_age = db.Column(db.Integer)
    animal_status = db.Column(db.String(20))
    current_weight = db.Column(db.Float)
    date_of_birth = db.Column(db.Date)
    date_of_arrival = db.Column(db.Date)
    animal_type = db.Column(db.String(50))
    coat_type = db.Column(db.String(50))
    primary_color = db.Column(db.String(50))
    secondary_color = db.Column(db.String(50))
    breed = db.Column(db.String(50))
    gender = db.Column(db.String(10))