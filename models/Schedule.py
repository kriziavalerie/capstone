from app_factory import db

class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_applied = db.Column(db.Date)
    time_applied = db.Column(db.String(8))
    note = db.Column(db.String(255))  # You can adjust the length as needed

