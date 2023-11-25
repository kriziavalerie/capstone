from app_factory import db


class AnimalHealth(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    animal_id = db.Column(db.Integer, db.ForeignKey('animal.id'), nullable=False)
    health_type = db.Column(db.String(50))
    dose = db.Column(db.String(20))
    frequency = db.Column(db.String(20))
    rabies_vaccination = db.Column(db.String(20))
    deworming = db.Column(db.String(20))
    health_frequency = db.Column(db.String(20))
