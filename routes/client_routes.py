from flask import Blueprint, render_template, redirect, url_for, session,flash,request
from app_factory import db, bcrypt
from models.Client import Client
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from models.Animal import Animal
from models.AnimalDetail import AnimalDetails
from models.AnimalStory import AnimalStory
from models.AnimalHealth import AnimalHealth
from models.ClientAnimal import ClientAnimal
from models.Client import Client
from models.Volunteer import Volunteer
from app_factory import app
import os
from werkzeug.utils import secure_filename


client_blueprint = Blueprint('client', __name__)

# Dashboard Route for Client
@client_blueprint.route('/client_dashboard')
def client_dashboard():
    if 'username' in session:
 
        return render_template('client_dashboard.html')
    else:
        return redirect(url_for('auth.login'))


@client_blueprint.route('/my_profile')
def show_my_profile():
    if 'username' in session:
        user_id = session['user_id']
        avatar = session.get('avatar')  # Get the avatar from the session, or None if it's not set
        client = Client.query.get(user_id)
        animal_details = AnimalDetails.query.all()
        animals = Animal.query.all()
        volunteers = Volunteer.query.filter_by(client_id = user_id).all()

        
        # Query ClientAnimal data for the specific client
        client_animals = ClientAnimal.query.filter_by(client_id=user_id).all()
        
        return render_template('my_profile.html', client=client, avatar=avatar, client_animals=client_animals,animal_details = animal_details,animals = animals,volunteers = volunteers)
    else:
        return redirect(url_for('auth.login'))


@client_blueprint.route('/client_edit_client_animal/<int:client_id>/<int:animal_id>', methods=['GET', 'POST'])
def client_edit_client_animal(client_id, animal_id):
    if 'username' in session:
        # Fetch the specific client animal record based on client_id and animal_id
        client_animal = ClientAnimal.query.filter_by(client_id=client_id, animal_id=animal_id).first()

        if request.method == 'POST':
            try:
                # Update the client animal record with the new data from the form
                # You can access form data like request.form['form_field_name']
                date_applied_str = request.form.get('appointment_date')
                new_time_applied_str = request.form.get('time_applied')

                # Parse the date string into a Python date object
                date_applied = datetime.strptime(date_applied_str, "%Y-%m-%d")

                # Update the appointment_date field
                client_animal.appointment_date = date_applied
                client_animal.time_applied = new_time_applied_str

                # Commit the changes to the database
                db.session.commit()

                # Redirect to a success page or another route
                return redirect(url_for('client.show_my_profile'))
            except ValueError:
                # Handle the case where the date format is invalid
                flash('Invalid date format. Please use the format YYYY-MM-DD.', 'error')

        # Render the edit template with the client animal data
        return render_template('my_profile.html', client_animal=client_animal)
    else:
        return redirect(url_for('auth.login'))
    
@client_blueprint.route('/edit_reasons_to_qualify', methods=['GET', 'POST'])
def edit_reasons_to_qualify():
    if 'user_id' in session:
        user_id = session['user_id']
        client = Client.query.get(user_id)

        if client:
            if request.method == 'POST':
                new_reasons_to_qualify = request.form.get('reason_to_qualify')

                # Update the "reasons_to_qualify" attribute
                client.reason_to_qualify = new_reasons_to_qualify

                # Save the changes to the database
                db.session.commit()

                flash('Reasons to qualify updated successfully', 'success')
                return redirect(url_for('client.show_my_profile'))

            elif request.method == 'GET':
                return render_template('edit_reasons_to_qualify.html', client=client)

        flash('User not found.', 'danger')
        return redirect(url_for('auth.login'))
    else:
        flash('User not authenticated.', 'danger')
        return redirect(url_for('auth.login'))
 

@client_blueprint.route('/pets')
def pets():
    if 'username' in session:
        user_id = session['user_id']  # Get the user_id from the session
        client = Client.query.get(user_id)  # Retrieve the Client object based on user_id
        if client:
            # Retrieve ClientAnimal objects associated with the client
            client_animals = ClientAnimal.query.filter_by(client_id=user_id).all()

            # Retrieve all Animal and AnimalDetails objects
        # Subquery to select the `animal_id` from `ClientAnimal` records with the status 'accept'
            subquery = db.session.query(ClientAnimal.animal_id).filter(ClientAnimal.status == 'accept')

            # Query to get all Animal objects that are not associated with the 'accept' status
            animals = Animal.query.filter(~Animal.id.in_(subquery)).all()

            animal_details = AnimalDetails.query.all()

            return render_template('pets.html', animals=animals, animal_details=animal_details, client=client, client_animals=client_animals)
        else:
            flash('Client not found.', 'danger')
            return redirect(url_for('auth.login'))
    else:
        return redirect(url_for('auth.login'))



@client_blueprint.route('/pet/details/<int:animal_id>')
def pet_details(animal_id):
    if 'username' in session:
        # Retrieve the Animal object with the specified animal_id
        animal = Animal.query.get(animal_id)
        
        # Retrieve the AnimalStory object with the same animal_id
        animal_story = AnimalStory.query.filter_by(animal_id=animal_id).first()
        animal_detail = AnimalDetails.query.filter_by(animal_id=animal_id).first()


        if animal:
            return render_template('pet_details.html', animal=animal, animal_story=animal_story,animal_detail=animal_detail)
        else:
            return redirect(url_for('client.pets'))

    else:
        return redirect(url_for('auth.login'))
    
@client_blueprint.route('/pet/personal_details/<int:animal_id>')
def personal_details(animal_id):
    if 'username' in session:
        # Retrieve the Animal object with the specified animal_id
        animal = Animal.query.get(animal_id)
        
        # Retrieve the AnimalDetails object with the same animal_id
        animal_detail = AnimalDetails.query.filter_by(animal_id=animal_id).first()
        
        # Retrieve the AnimalHealth object with the same animal_id
        animal_health = AnimalHealth.query.filter_by(animal_id=animal_id).first()

        if animal:
            return render_template('personal_details.html', animal=animal, animal_detail=animal_detail, animal_health=animal_health)
        else:
            return redirect(url_for('client.pets'))
    else:
        return redirect(url_for('auth.login'))

    
@client_blueprint.route('/client_volunteers')
def client_volunteers():
    if 'username' in session:
        user_id = session['user_id']

        return render_template('client_volunteers.html',user_id = user_id)
    else:
        return redirect(url_for('auth.login'))

@client_blueprint.route('/volunteer/add/apply', methods=['POST'])
def apply():
    if 'user_id' in session:
        user_id = session['user_id']
        client = Client.query.get(user_id)

        if client:
            new_date_applied_str = request.form.get('date_applied')
            new_time_applied_str = request.form.get('time_applied')

            # Parse the date string into a Python date object
            new_date_applied = datetime.strptime(new_date_applied_str, "%Y-%m-%d")

            # Store the time as a string in the format 'HH:MM'
            new_time_applied = new_time_applied_str

            # Create a new Volunteer entry
            volunteer = Volunteer(client_id=client.id, date_applied=new_date_applied, time_applied=new_time_applied, application_status='pending')

            # Add the new volunteer entry to the database
            db.session.add(volunteer)

            # Commit the changes to the database
            db.session.commit()

            flash('Applied successfully', 'success')
            return redirect(url_for('client.client_volunteers'))

        flash('User not found.', 'danger')
        return redirect(url_for('auth.login'))

    flash('User not authenticated.', 'danger')
    return redirect(url_for('auth.login'))


@client_blueprint.route('/settings', methods=['GET', 'POST'])
def settings():
    if 'user_id' in session:
        user_id = session['user_id']
        avatar = session.get('avatar')  # Get the avatar from the session, or None if it's not set
        client = Client.query.get(user_id)  # Assuming you have a Client model

        if client:
            if request.method == 'POST':
                # Retrieve data from the form and update client information
                client.first_name = request.form.get('first_name', client.first_name)
                client.last_name = request.form.get('last_name', client.last_name)
                client.email = request.form.get('email', client.email)
                client.age = request.form.get('age', client.age)
                client.address = request.form.get('address', client.address)
                client.contact_number = request.form.get('contact_number', client.contact_number)
                
                # Format the date_applied if it's not empty
                date_applied_str = request.form.get('date_applied')
                if date_applied_str:
                    date_applied = datetime.strptime(date_applied_str, '%Y-%m-%d')
                    client.date_applied = date_applied
                else:
                    client.date_applied = None  # Set to None if the date is empty

                client.reason_to_qualify = request.form.get('reason_to_qualify', client.reason_to_qualify)

                # Save the changes to the database
                db.session.commit()

                flash('Client information updated successfully', 'success')
                return redirect(url_for('client.settings'))
            elif request.method == 'GET':
                # Determine if the password is null and pass it to the template
                password_null = client.password is None
                return render_template('settings.html', client=client, password_null=password_null, avatar=avatar)
        else:
            flash('Client not found.', 'danger')
            return redirect(url_for('auth.login'))
    else:
        flash('User not authenticated.', 'danger')
        return redirect(url_for('auth.login'))
    
@client_blueprint.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if 'user_id' in session:
        user_id = session['user_id']
        user = Client.query.get(user_id)

        if user:
            if request.method == 'POST':
                # Handle password change
                old_password = request.form.get('old_password')
                new_password = request.form.get('password')
                confirm_password = request.form.get('confirm_password')

                if not old_password:
                    flash('Please enter your old password.', 'danger')
                elif not new_password:
                    flash('Please enter a new password.', 'danger')
                elif new_password != confirm_password:
                    flash('New password and confirmation do not match.', 'danger')
                elif not bcrypt.check_password_hash(user.password, old_password):
                    flash('Incorrect old password. Password not changed.', 'danger')
                else:
                    # Update the user's password with the hashed version
                    hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
                    user.password = hashed_password

                    # Save the changes to the database
                    db.session.commit()

                    flash('Password changed successfully', 'success')
                    return redirect(url_for('settings'))
                return redirect(url_for('client.settings'))
                
            elif request.method == 'GET':
                password_null = user.password is None
                return render_template('settings.html', user=user, password_null=password_null)

        flash('User not found.', 'danger')
        return redirect(url_for('auth.login'))
    else:
        flash('User not authenticated.', 'danger')
        return redirect(url_for('auth.login'))


@client_blueprint.route('/change_email', methods=['GET', 'POST'])
def change_email():
    if 'user_id' in session:
        user_id = session['user_id']
        user = Client.query.get(user_id)

        if user:
            if request.method == 'POST':
                new_email = request.form.get('new_email_address')

                if not new_email:
                    flash('Please enter a new email address.', 'danger')
                elif new_email == user.email:
                    flash('The new email address is the same as the current one.', 'danger')
                else:
                    try:
                        # Attempt to update the user's email address
                        user.email = new_email

                        # Save the changes to the database
                        db.session.commit()

                        flash('Email address changed successfully', 'success')
                        return redirect(url_for('client.settings'))

                    except IntegrityError:
                        db.session.rollback()  # Roll back the transaction
                        flash('Email address is already taken. Please try another email.', 'danger')
                        return redirect(url_for('client.settings'))


            elif request.method == 'GET':
                return render_template('change_email.html', user=user)
    
        flash('User not found.', 'danger')
        return redirect(url_for('client.settings'))
    else:
        flash('User not authenticated.', 'danger')
        return redirect(url_for('auth.login'))
    
@client_blueprint.route('/add_to_pawmily/<int:animal_id>', methods=['GET'])
def add_to_pawmily(animal_id):
    if 'user_id' in session:
        user_id = session['user_id']
        
        # Count the number of existing ClientAnimal associations for the client
        client_animal_count = ClientAnimal.query.filter_by(client_id=user_id).count()

        if client_animal_count >= 2:
            flash('You can only apply for a maximum of 2 pets at a time.', 'danger')
        else:
            client = Client.query.get(user_id)  # Assuming you have a Client model
            animal = Animal.query.get(animal_id)  # Assuming you have an Animal model

            if client and animal:
                # Create a new ClientAnimal association
                client_animal = ClientAnimal(client_id=user_id, animal_id=animal_id)
                
                # Add the association to the database
                db.session.add(client_animal)
                db.session.commit()

                flash('Added to Pawmily', 'success')
            else:
                flash('Client or Animal not found.', 'danger')
    else:
        flash('User not authenticated.', 'danger')

    return redirect(url_for('client.pets'))

@client_blueprint.route('/remove_from_pawmily/<int:animal_id>', methods=['GET'])
def remove_from_pawmily(animal_id):
    if 'user_id' in session:
        user_id = session['user_id']

        client = Client.query.get(user_id)
        animal = Animal.query.get(animal_id)

        if client and animal:
            # Check if the pet is part of the client's Pawmily
            client_animal = ClientAnimal.query.filter_by(client_id=user_id, animal_id=animal_id).first()

            if client_animal:
                # Remove the association from the database
                db.session.delete(client_animal)
                db.session.commit()

                flash('Removed from Pawmily', 'success')
            else:
                flash('This pet is not in your Pawmily.', 'danger')
        else:
            flash('Client or Animal not found.', 'danger')
    else:
        flash('User not authenticated.', 'danger')

    return redirect(url_for('client.pets'))

@client_blueprint.route('/apply_pets', methods=['POST'])
def apply_pets():
    if 'user_id' in session:
        user_id = session['user_id']
        selected_pet_ids = request.form.getlist('pet_ids')
        client = Client.query.get(user_id)

        if client.reason_to_qualify is None or not client.reason_to_qualify.strip():
            flash('Please provide a reason to qualify for pet adoption in your profile.', 'danger')
            return redirect(url_for('client.settings'))
        
        if len(selected_pet_ids) > 2:
            flash('You can only apply for a maximum of 2 pets at a time.', 'danger')

        if not(selected_pet_ids):
            flash('Select the Pet that you want to apply(check the checkbox near the pet)','danger')
            return redirect(url_for('client.pets'))
        else:
            # Apply for the selected pets by updating their status
            for pet_id in selected_pet_ids:
                client_animal = ClientAnimal.query.filter_by(client_id=user_id, animal_id=pet_id).first()
                if client_animal:
                    client_animal.status = 'pending'
                    date_applied = datetime.now()
                    date_string = date_applied.strftime("%Y-%m-%d")
                    date_applied_date = datetime.strptime(date_string, "%Y-%m-%d").date()
                    client_animal.date_applied = date_applied_date
                    db.session.commit()
            
            flash('Pet applications submitted and pending approval', 'success')
            return redirect(url_for('client.show_my_profile'))
    else:
        flash('User not authenticated.', 'danger')

    return redirect(url_for('client.pets'))

@client_blueprint.route('/client/update/<int:id>', methods=['POST'])
def update_client(id):
    client = Client.query.get_or_404(id)
    if 'image_path' in request.files:
        image = request.files['image_path']
        if image:
            # Ensure the upload folder exists
            upload_folder = app.config['UPLOAD_FOLDER']
            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)

            # Handle duplicate filenames
            filename = secure_filename(image.filename)
            name, ext = os.path.splitext(filename)
            counter = 1
            while os.path.exists(os.path.join(upload_folder, filename)):
                filename = f"{name}({counter}){ext}"
                counter += 1

            # Save the uploaded image to the upload folder
            image.save(os.path.join(upload_folder, filename))

            # Store the relative image path in the database
            relative_image_path = os.path.join('uploaded_images', filename).replace('\\', '/')  # Assuming 'uploaded_images' is the directory
            client.image_path = relative_image_path
            db.session.commit()

            flash('Client updated successfully', 'success')
            return redirect(url_for('client.settings'))

    flash('Client update failed. Image not found.', 'error')
    return redirect(url_for('client.setings'))
