from app_factory import db


class Animal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_path = db.Column(db.String(200))  # Adjust the length as needed
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=True)

    # Define one-to-one relationships with other models
    details = db.relationship('AnimalDetails', backref='animal', uselist=False)
    health = db.relationship('AnimalHealth', backref='animal', uselist=False)
    owner = db.relationship('AnimalOwner', backref='animal', uselist=False)
    story = db.relationship('AnimalStory', backref='animal', uselist=False)
    clients = db.relationship('ClientAnimal', back_populates='animal')