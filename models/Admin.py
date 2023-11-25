from app_factory import db

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, name="unique_email_constraint")
    username = db.Column(db.String(20), unique=True, nullable=False)  # 
    password = db.Column(db.String(60), nullable=False)