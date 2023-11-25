from flask import Blueprint, render_template, redirect, url_for, request, flash
from app_factory import db
from models.Animal import Animal
from models.AnimalHealth import AnimalHealth

animal_health_blueprint = Blueprint('animal_health', __name__)


# Animal Health Route
@animal_health_blueprint.route('/animal/health/create', methods=['POST'])
def create_animal_health():
    if request.method == 'POST':
        animal_id = request.form.get('animal_id')
        animal = Animal.query.get(animal_id)
        health_type = request.form.get('health_type')
        dose = request.form.get('dose')
        frequency = request.form.get('frequency')
        rabies_vaccination = request.form.get('rabies_vaccination')
        deworming = request.form.get('deworming')
        health_frequency = request.form.get('health_frequency')

        # Validation checks
        errors = []

        if not animal_id:
            errors.append('Choose Pet Image first')
        if not health_type:
            errors.append('Health type is required.')
        # Add more validation checks for other fields

        if errors:
            for error in errors:
                flash(error, 'danger')
        else:
            # Create and add the animal health record if there are no validation errors
            animal_health = AnimalHealth(
                animal_id=animal_id,
                health_type=health_type,
                dose=dose,
                frequency=frequency,
                rabies_vaccination=rabies_vaccination,
                deworming=deworming,
                health_frequency=health_frequency
            )

            db.session.add(animal_health)
            db.session.commit()
            flash('Animal health record created successfully', 'success')

    # # # Redirect to a suitable page after creating the health record
    # # return redirect(url_for('admin.show_animals'))
    # return render_template('add_animal.html',
    #                        animal_id=animal_id,
    #                        health_type=health_type,
    #                        dose=dose,
    #                        frequency=frequency,
    #                        rabies_vaccination=rabies_vaccination,
    #                        deworming=deworming,
    #                        health_frequency=health_frequency,
    #                        relative_image_path=animal.image_path
    #                        )
        return redirect(url_for('admin.show_animals'))


@animal_health_blueprint.route('/animal/health/edit/<int:animal_id>', methods=['GET', 'POST'])
def edit_animal_health(animal_id):
    # Find the existing animal health detail by its animal_id
    animal_health = AnimalHealth.query.filter_by(animal_id=animal_id).first()

    # Find the existing animal by its ID
    animal = Animal.query.get(animal_id)

    if request.method == 'POST':
        # Retrieve form data for editing
        health_type = request.form.get('health_type')
        dose = request.form.get('dose')
        frequency = request.form.get('frequency')
        rabies_vaccination = request.form.get('rabies_vaccination')
        deworming = request.form.get('deworming')
        health_frequency = request.form.get('health_frequency')

        if animal_health:
            # If animal_health record exists, update it
            animal_health.health_type = health_type
            animal_health.dose = dose
            animal_health.frequency = frequency
            animal_health.rabies_vaccination = rabies_vaccination
            animal_health.deworming = deworming
            animal_health.health_frequency = health_frequency
        else:
            # If animal_health record does not exist, create a new one
            new_animal_health = AnimalHealth(
                animal_id=animal_id,
                health_type=health_type,
                dose=dose,
                frequency=frequency,
                rabies_vaccination=rabies_vaccination,
                deworming=deworming,
                health_frequency=health_frequency
            )
            db.session.add(new_animal_health)

        db.session.commit()
        flash('Animal health details updated successfully', 'success')
        return redirect(url_for('admin.show_animals'))

    # Render the edit template with the existing animal and animal_health
    return render_template('edit_animal.html', animal=animal, animal_health=animal_health)
