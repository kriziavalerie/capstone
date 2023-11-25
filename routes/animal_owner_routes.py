from flask import Blueprint, render_template, redirect, url_for, request, flash
from app_factory import db
from models.AnimalOwner import AnimalOwner
from models.Animal import Animal
from datetime import datetime

animal_owner_blueprint = Blueprint('animal_owner', __name__)
    #Animal Owner Routes
@animal_owner_blueprint.route('/animal/owner/create', methods=['POST'])
def create_animal_owner():
    # Retrieve form data for creating an AnimalOwner
    animal_id = request.form.get('animal_id')
    name = request.form.get('name')
    address = request.form.get('address')
    contact_number = request.form.get('contact_number')
    email_address = request.form.get('email_address')
    age = request.form.get('age')
    date_applied_str = request.form.get('date_applied')
    date_adopted_str = request.form.get('date_adopted')
    animal = Animal.query.get(animal_id)

        
    if date_applied_str:
        date_applied = datetime.strptime(date_applied_str, '%Y-%m-%d')
    else:
        date_applied = None

    if date_adopted_str:
        date_adopted = datetime.strptime(date_adopted_str, '%Y-%m-%d')
    else:
        date_adopted = None
    

    # Perform basic validation
    if not animal_id or not name:
        flash('Animal ID and Name are required', 'danger')
        return render_template('animal_owner_form.html')  # Render the 'animal_owner_form.html' template with an error message

    # You can add additional validation here if needed
    # For example, you can check if the provided animal_id exists in your database.

    # Create a new AnimalOwner object and add it to the database
    animal_owner = AnimalOwner(
        animal_id=animal_id,
        name=name,
        address=address,
        contact_number=contact_number,
        email_address=email_address,
        age=age,
        date_applied=date_applied,
        date_adopted=date_adopted
    )
    db.session.add(animal_owner)
    db.session.commit()

    # Flash a success message and redirect to a relevant page
    flash('Animal Owner created successfully', 'success')
    
    # # Redirect to a suitable page after creating the health record
    # return redirect(url_for('admin.show_animals'))
    return render_template('add_animal.html',
                               animal_id=animal_id,
                                name=name,
                                address=address,
                                contact_number=contact_number,
                                email_address=email_address,
                                age=age,
                                date_applied=date_applied,
                                date_adopted=date_adopted,
                                relative_image_path=animal.image_path
                           )


# Animal Owner Edit or Create Route
@animal_owner_blueprint.route('/animal/owner/edit/<int:id>', methods=['GET', 'POST'])
def edit_animal_owner(id):
    # Find the existing animal owner by its ID
    animal_owner = AnimalOwner.query.get(id)

    if animal_owner:
        if request.method == 'POST':
            # Retrieve form data for editing
            animal_id = request.form.get('animal_id')
            name = request.form.get('name')
            address = request.form.get('address')
            contact_number = request.form.get('contact_number')
            email_address = request.form.get('email_address')
            age = request.form.get('age')

            # Check if date fields are empty or not
            date_applied_str = request.form.get('date_applied')
            date_adopted_str = request.form.get('date_adopted')

            if date_applied_str:
                date_applied = datetime.strptime(date_applied_str, '%Y-%m-%d')
            else:
                date_applied = None

            if date_adopted_str:
                date_adopted = datetime.strptime(date_adopted_str, '%Y-%m-%d')
            else:
                date_adopted = None

            # Perform basic validation
            if not animal_id or not name:
                flash('Animal ID and Name are required', 'danger')
                return redirect(url_for('admin.show_animals'))

            # Check if the provided animal_id exists in the database
            existing_animal = Animal.query.get(animal_id)
            if not existing_animal:
                flash('Animal with the provided ID does not exist', 'danger')
                return redirect(url_for('admin.show_animals'))

            # Check if there is already an owner for the provided animal_id
            existing_owner = AnimalOwner.query.filter_by(animal_id=animal_id).first()
            if existing_owner and existing_owner.id != id:
                flash('There is already an owner for this animal', 'danger')
                return redirect(url_for('admin.show_animals'))

            # Update the existing AnimalOwner object
            animal_owner.animal_id = animal_id
            animal_owner.name = name
            animal_owner.address = address
            animal_owner.contact_number = contact_number
            animal_owner.email_address = email_address
            animal_owner.age = age
            animal_owner.date_applied = date_applied
            animal_owner.date_adopted = date_adopted

            db.session.commit()
            flash('Animal Owner details updated successfully', 'success')
            return redirect(url_for('admin.show_animals'))

        # Render the edit template with the existing animal owner
        return render_template('edit_animal_owner.html', animal_owner=animal_owner)
    else:
        flash('Animal Owner not found', 'danger')
        return redirect(url_for('admin.show_animals'))

