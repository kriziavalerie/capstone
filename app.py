
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from sqlalchemy.exc import IntegrityError
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask import request
from werkzeug.utils import secure_filename
from datetime import datetime
import os
import app_factory
from routes import admin_routes, animal_health_routes, animal_owner_routes, animal_routes, animal_story_routes, auth_routes, client_routes, animal_details_routes, google_oauth_routes
from flask_oauthlib.client import OAuth
from app_factory import db, bcrypt
from models.Admin import Admin
from models.Schedule import Schedule
from datetime import datetime, timedelta

app = app_factory.app
oauth = OAuth(app)

# Another code that will trigger everytime for the notication
# def create_notifications():
#     current_time = datetime.now()
#     schedules = Schedule.query.all()

#     for schedule in schedules:
#         notification_time = datetime.combine(schedule.date_applied, datetime.strptime(schedule.time_applied, '%H:%M').time())

#         # Calculate time differences
#         time_until_notification = notification_time - current_time
#         one_day_before = timedelta(days=1)
#         thirty_minutes_before = timedelta(minutes=30)
#         five_minutes_before = timedelta(minutes=5)

#         # code that will trigger every time 
#         if time_until_notification < one_day_before:
#             flash(f"One day before: {schedule.note}")
#         elif time_until_notification < thirty_minutes_before:
#             flash(f"30 minutes before: {schedule.note}")
#         elif time_until_notification < five_minutes_before:
#             flash(f"5 minutes before: {schedule.note}")

 # Function to create notifications
def create_notifications():
    current_time = datetime.now()
    schedules = Schedule.query.all()
    
    # Get the list of schedule IDs for which notifications have already been flashed
    flashed_schedule_ids = session.get('flashed_schedule_ids', [])

    for schedule in schedules:
        # Calculate time differences
        notification_time = datetime.combine(schedule.date_applied, datetime.strptime(schedule.time_applied, '%H:%M').time())
        time_until_notification = notification_time - current_time
        one_day_before = timedelta(days=1)
        thirty_minutes_before = timedelta(minutes=30)
        five_minutes_before = timedelta(minutes=5)

        # Check if it's time to send a notification and if it hasn't been flashed already
        if time_until_notification < one_day_before and schedule.id not in flashed_schedule_ids:
            flash(f"One day before: {schedule.note}")
            flashed_schedule_ids.append(schedule.id)
        elif time_until_notification < thirty_minutes_before and schedule.id not in flashed_schedule_ids:
            flash(f"30 minutes before: {schedule.note}")
            flashed_schedule_ids.append(schedule.id)
        elif time_until_notification < five_minutes_before and schedule.id not in flashed_schedule_ids:
            flash(f"5 minutes before: {schedule.note}")
            flashed_schedule_ids.append(schedule.id)
    
    # Update the flashed_schedule_ids list in the session
    session['flashed_schedule_ids'] = flashed_schedule_ids
         
# Register the create_notifications function to run before each request in the admin blueprint
@app.before_request
def before_admin_request():
    if request.blueprint == 'admin':
        create_notifications()

app.register_blueprint(admin_routes.admin_blueprint)
app.register_blueprint(animal_health_routes.animal_health_blueprint)
app.register_blueprint(animal_owner_routes.animal_owner_blueprint)
app.register_blueprint(animal_routes.animal_blueprint)
app.register_blueprint(animal_story_routes.animal_story_blueprint)
app.register_blueprint(auth_routes.auth_blueprint)
app.register_blueprint(client_routes.client_blueprint)
app.register_blueprint(animal_details_routes.animal_details_blueprint)
app.register_blueprint(google_oauth_routes.google_oauth_blueprint, url_prefix='/google')


# # Create the admin user
# admin_password = 'tails_of_freedom'
# hashed_password = bcrypt.generate_password_hash(admin_password).decode('utf-8')
# admin = Admin(
#     first_name='Admin',
#     last_name='User',
#     email='admin@example.com',
#     username='admin',
#     password=hashed_password
# )

# # Add the admin user to the database
# with app.app_context():
#     db.create_all()
#     db.session.add(admin)
#     db.session.commit()




if __name__ == '__main__':
    app.run(debug=True)
