from app_factory import db

class Volunteer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id', name='fk_volunteer_client_id'))
    date_applied = db.Column(db.Date)
    time_applied = db.Column(db.String(8))
    application_status = db.Column(db.String(20))  # Pending, Approved, Declined

    # Define a relationship with the Client model
    client = db.relationship('Client', back_populates='volunteers')