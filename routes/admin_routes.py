# admin_routes.py

from sqlalchemy import not_
from flask import Blueprint, render_template, redirect, url_for, session,request,flash
from app_factory import db
from models.Animal import Animal
from models.Admin import Admin
from models.Client import Client
from models.AnimalDetail import AnimalDetails
from models.ClientAnimal import ClientAnimal
from models.Volunteer import Volunteer
from models.Schedule import Schedule
from datetime import datetime,timedelta
from sqlalchemy.exc import IntegrityError

admin_blueprint = Blueprint('admin', __name__)

@admin_blueprint.route('/admin_dashboard')
def admin_dashboard():
    if 'username' in session:
        return render_template('admin_dashboard.html')
    else:
        return redirect(url_for('auth.login'))

@admin_blueprint.route('/animals')
def show_animals():
    if 'username' in session:
        # Fetch all animals and their details from the database
        animals = Animal.query.all()
        animal_details = AnimalDetails.query.all()


        # Render the Animals template with the list of animals and their details
        return render_template('animals.html', animals=animals, animal_details=animal_details)
    else:
        return redirect(url_for('auth.login'))

@admin_blueprint.route('/client_information')
def show_clients():
    if 'username' in session:
        # Fetch all clients from the database
        clientanimals= ClientAnimal.query.filter(not_(ClientAnimal.status.is_(None))).all()
        
        
        # Render the Clients template with the list of clients
        return render_template('client_information.html', clientanimals=clientanimals)
    else:
        return redirect(url_for('auth.login'))


@admin_blueprint.route('/edit_client_animal/<int:client_id>/<int:animal_id>', methods=['GET', 'POST'])
def edit_client_animal(client_id, animal_id):
    if 'username' in session:
        # Fetch the specific client animal record based on client_id and animal_id
        client_animal = ClientAnimal.query.filter_by(client_id=client_id, animal_id=animal_id).first()

        if request.method == 'POST':
            # Update the client animal record with the new data from the form
            # You can access form data like request.form['form_field_name']
            client_animal.status = request.form['status']

            # Commit the changes to the database
            db.session.commit()
            
            # Redirect to a success page or another route
            return redirect(url_for('admin.show_clients'))

        # Render the edit template with the client animal data
        return render_template('client_information_details.html', client_animal=client_animal)
    else:
        return redirect(url_for('auth.login'))
    
@admin_blueprint.route('/volunteers')
def show_volunteers():
    if 'username' in session:
        # Retrieve all volunteers
        volunteers = Volunteer.query.all()
        
        return render_template('volunteers.html', volunteers=volunteers)
    else:
        return redirect(url_for('auth.login'))
    

@admin_blueprint.route('/volunteers/edit/<int:volunteer_id>', methods=['GET', 'POST'])
def edit_volunteer(volunteer_id):
    if 'username' in session:
        # Retrieve the volunteer by volunteer_id
        volunteer = Volunteer.query.get(volunteer_id)

        if volunteer:
            if request.method == 'POST':
                new_status = request.form.get('status')

                # Update the status attribute
                volunteer.application_status = new_status

                # Save the changes to the database
                db.session.commit()

                flash('Status updated successfully', 'success')
                return redirect(url_for('admin.show_volunteers'))

            elif request.method == 'GET':
                return render_template('edit_volunteer.html', volunteer=volunteer)

        flash('Volunteer not found.', 'danger')
        return redirect(url_for('admin.show_volunteers'))
    else:
        flash('User not authenticated.', 'danger')
        return redirect(url_for('auth.login'))
    
    
admin_blueprint.route('/schedules/edit/<int:schedule_id>', methods=['POST'])
def edit_schedule(schedule_id):
    if 'username' in session:
        schedule = Schedule.query.get(schedule_id)
        if schedule:
            # Parse the date string into a Python date object
            date_applied_str = request.form.get('date_applied_schedule')
            date_applied = datetime.strptime(date_applied_str, "%Y-%m-%d")

            # Store the time as a string in the format 'HH:MM'
            time_applied = request.form.get('time_applied_schedule')

            # Update schedule attributes
            schedule.date_applied = date_applied
            schedule.time_applied = time_applied
            schedule.note = request.form.get('note')

            # Save the changes to the database
            db.session.commit()

            flash('Schedule updated successfully', 'success')
        else:
            flash('Schedule not found for editing.', 'danger')

        return redirect(url_for('admin.manage_schedules'))

    flash('User not authenticated.', 'danger')
    return redirect(url_for('auth.login'))

@admin_blueprint.route('/schedules', methods=['GET'])
def manage_schedules():
    if 'username' in session:
        if request.method == 'GET':
            # Retrieve all schedules from the database
            schedules = Schedule.query.all()
            return render_template('schedules.html', schedules=schedules)

    flash('User not authenticated.', 'danger')
    return redirect(url_for('auth.login'))


@admin_blueprint.route('/schedules/create', methods=['POST'])
def create_schedule():
    if 'username' in session:
        if request.method == 'POST':
            date_applied_str = request.form.get('date_applied_schedule')
            time_applied_str = request.form.get('time_applied_schedule')
            note = request.form.get('note')

            # Parse the date string into a Python date object
            date_applied = datetime.strptime(date_applied_str, "%Y-%m-%d")

            # Store the time as a string in the format 'HH:MM'
            time_applied = time_applied_str

            # Check if a schedule with the same date and time applied already exists
            existing_schedule = Schedule.query.filter_by(date_applied=date_applied, time_applied=time_applied).first()

            if existing_schedule:
                flash('Schedule with the same date and time applied already exists', 'danger')
            else:
                # Create a new Schedule entry
                schedule = Schedule(date_applied=date_applied, time_applied=time_applied, note=note)

                try:
                    # Add the new schedule entry to the database
                    db.session.add(schedule)

                    # Commit the changes to the database
                    db.session.commit()

                    flash('Schedule created successfully', 'success')
                except IntegrityError as e:
                    flash('Error creating the schedule. Please check your input.', 'danger')
                    db.session.rollback()

            return redirect(url_for('admin.manage_schedules'))

    flash('User not authenticated.', 'danger')
    return redirect(url_for('auth.login'))


@admin_blueprint.route('/remove_schedule/<int:schedule_id>', methods=['POST'])
def remove_schedule(schedule_id):
    # Check if the schedule with the given ID exists and remove it
    schedule = Schedule.query.get(schedule_id)
    if schedule:
        db.session.delete(schedule)
        db.session.commit()
        flash('Schedule removed successfully', 'success')
    else:
        flash('Schedule not found for removal.', 'danger')

    return redirect(url_for('admin.manage_schedules'))
