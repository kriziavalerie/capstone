from flask import Blueprint, render_template, redirect, url_for, request, flash, session, send_from_directory
from datetime import datetime
from models.AnimalDetail import AnimalDetails
from models.Animal import Animal
from models.Admin import Admin
from models.Client import Client
from models.AnimalStory import AnimalStory
from models.AnimalOwner import AnimalOwner
from models.AnimalHealth import AnimalHealth
from app_factory import db

animal_details_blueprint = Blueprint('animal_details', __name__)

@animal_details_blueprint.route('/animal/details/create', methods=['POST'])
def create_animal_details():
    if request.method == 'POST':
        # Retrieve form data
        animal_id = request.form.get('animal_id')
        name = request.form.get('name')
        tag_number = request.form.get('tag_number')
        status = request.form.get('status')
        estimated_age = request.form.get('estimated_age')
        animal_status = request.form.get('animal_status')
        current_weight = request.form.get('current_weight')
           # Check if date fields are empty or not
        date_of_birth_str = request.form.get('date_of_birth')
        date_of_arrival_str = request.form.get('date_of_arrival')
        animal = Animal.query.get(animal_id)
        if date_of_birth_str:
            date_of_birth = datetime.strptime(date_of_birth_str, '%Y-%m-%d')
        else:
            date_of_birth = None

        if date_of_arrival_str:
            date_of_arrival = datetime.strptime(date_of_arrival_str, '%Y-%m-%d')
        else:
            date_of_arrival = None

        animal_type = request.form.get('animal_type')
        coat_type = request.form.get('coat_type')
        primary_color = request.form.get('primary_color')
        secondary_color = request.form.get('secondary_color')
        breed = request.form.get('breed')
        gender = request.form.get('gender')

        # Validation checks
        errors = []

        if not animal_id:
            errors.append('Add image of the pet first')
        if not name:
            errors.append('Name is required.')
        # Add more validation checks for other fields

        if errors:
            for error in errors:
                flash(error, 'danger')
        else:
            # Create and add the animal details if there are no validation errors
            animal_details = AnimalDetails(
                animal_id=animal_id,
                name=name,
                tag_number=tag_number,
                status=status,
                estimated_age=estimated_age,
                animal_status=animal_status,
                current_weight=current_weight,
                date_of_birth=date_of_birth,
                date_of_arrival=date_of_arrival,
                animal_type=animal_type,
                coat_type=coat_type,
                primary_color=primary_color,
                secondary_color=secondary_color,
                breed=breed,
                gender=gender,
            )

            db.session.add(animal_details)
            db.session.commit()
            flash('Animal details created successfully', 'success')
            return render_template('add_animal.html', 
                           animal_id=animal_id,
                           name=name,
                           tag_number=tag_number,
                           status=status,
                           estimated_age=estimated_age,
                           animal_status=animal_status,
                           current_weight=current_weight,
                           date_of_birth=date_of_birth_str if date_of_birth_str else '',
                           date_of_arrival=date_of_arrival_str if date_of_arrival_str else '',
                           animal_type=animal_type,
                           coat_type=coat_type,
                           primary_color=primary_color,
                           secondary_color=secondary_color,
                           breed=breed,
                           gender=gender,
                relative_image_path = animal.image_path
                           )

     # Render the template with the submitted form values for re-population
    return render_template('add_animal.html', 
                           animal_id=animal_id,
                           name=name,
                           tag_number=tag_number,
                           status=status,
                           estimated_age=estimated_age,
                           animal_status=animal_status,
                           current_weight=current_weight,
                           date_of_birth=date_of_birth_str if date_of_birth_str else '',
                           date_of_arrival=date_of_arrival_str if date_of_arrival_str else '',
                           animal_type=animal_type,
                           coat_type=coat_type,
                           primary_color=primary_color,
                           secondary_color=secondary_color,
                           breed=breed,
                           gender=gender)



@animal_details_blueprint.route('/animal/details/edit/<int:animal_id>', methods=['GET', 'POST'])
def edit_animal_details(animal_id):
    # Find the existing animal detail by its animal_id
    animal_detail = AnimalDetails.query.filter_by(animal_id=animal_id).first()
    
    # Find the existing animal by its ID
    animal = Animal.query.get(animal_id)
    animal_health = AnimalHealth.query.filter_by(animal_id=animal_id).first()
    animal_story = AnimalStory.query.filter_by(animal_id=animal_id).first()
    animal_owner = AnimalOwner.query.filter_by(animal_id = animal_id).first()
    clients = Client.query.all()

    if animal_detail and animal:
        if request.method == 'POST':
            # Retrieve form data for editing
            name = request.form.get('name')
            tag_number = request.form.get('tag_number')
            status = request.form.get('status')
            estimated_age = request.form.get('estimated_age')
            animal_status = request.form.get('animal_status')
            current_weight = request.form.get('current_weight')

            # Check if date fields are empty or not
            date_of_birth_str = request.form.get('date_of_birth')
            date_of_arrival_str = request.form.get('date_of_arrival')

            if date_of_birth_str:
                date_of_birth = datetime.strptime(date_of_birth_str, '%Y-%m-%d')
            else:
                date_of_birth = None

            if date_of_arrival_str:
                date_of_arrival = datetime.strptime(date_of_arrival_str, '%Y-%m-%d')
            else:
                date_of_arrival = None

            animal_type = request.form.get('animal_type')
            coat_type = request.form.get('coat_type')
            primary_color = request.form.get('primary_color')
            secondary_color = request.form.get('secondary_color')
            breed = request.form.get('breed')
            gender = request.form.get('gender')

            # Update the existing animal details
            animal_detail.name = name
            animal_detail.tag_number = tag_number
            animal_detail.status = status
            animal_detail.estimated_age = estimated_age
            animal_detail.animal_status = animal_status
            animal_detail.current_weight = current_weight
            animal_detail.date_of_birth = date_of_birth
            animal_detail.date_of_arrival = date_of_arrival
            animal_detail.animal_type = animal_type
            animal_detail.coat_type = coat_type
            animal_detail.primary_color = primary_color
            animal_detail.secondary_color = secondary_color
            animal_detail.breed = breed
            animal_detail.gender = gender
            db.session.commit()
            flash('Animal details updated successfully', 'success')
            return redirect(url_for('admin.show_animals'))
    
        # Render the edit template with the existing animal and animal_detail
        return render_template('edit_animal.html', animal=animal, animal_detail=animal_detail,animal_health=animal_health,relative_image_path=animal.image_path,animal_story=animal_story,clients = clients,animal_owner=animal_owner)
    else:
        flash('Animal details not found', 'danger')
        if animal:
             return render_template('add_animal.html', relative_image_path=animal.image_path, animal_id=animal_id,clients = clients)
        else:
            return redirect(url_for('admin.show_animals'))
