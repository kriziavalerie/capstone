from flask import Blueprint, render_template, redirect, url_for, request, flash, session, send_from_directory, make_response,send_file
from app_factory import db
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from app_factory import app
from models.AnimalDetail import AnimalDetails
from models.Animal import Animal
from models.AnimalStory import AnimalStory
from models.AnimalOwner import AnimalOwner
from models.Client import Client
from models.AnimalHealth import AnimalHealth
import pdfkit

animal_blueprint = Blueprint('animal', __name__)

pdfkit_config = pdfkit.configuration(wkhtmltopdf='C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')
#ANIMAL ROUTES

@animal_blueprint.route('/animal/create', methods=['POST'])
def create_animal():
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
            animal = Animal(image_path=relative_image_path)
            db.session.add(animal)
            db.session.commit()

            # Retrieve the ID of the newly inserted record
            animal_id = animal.id

            flash('Animal created successfully', 'success')
            clients= Client.query.all()
            return render_template('add_animal.html',relative_image_path=relative_image_path,animal_id=animal_id,clients = clients)

        else:
            flash('No image selected for upload', 'error')
    else:
        flash('Image upload failed. Image not found.', 'error')

    return render_template('add_animal.html')

@animal_blueprint.route('/animal/update/<int:id>', methods=['POST'])
def update_animal(id):
    animal = Animal.query.get_or_404(id)
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
            animal.image_path = relative_image_path
            db.session.commit()

            flash('Animal updated successfully', 'success')
            return redirect(url_for('admin.show_animals'))


    flash('Animal update failed. Image not found.', 'error')
    return redirect(url_for('admin.add_animal'))

@animal_blueprint.route('/animal/delete/<int:id>', methods=['POST'])
def delete_animal(id):
    try:
        animal = Animal.query.get_or_404(id)

        # Add more validation and authorization checks here

        # Delete associated data from AnimalDetail
        animal_details_to_delete = AnimalDetails.query.filter_by(animal_id=id).all()
        for detail in animal_details_to_delete:
            db.session.delete(detail)

        # Delete associated data from AnimalHealth
        animal_health_to_delete = AnimalHealth.query.filter_by(animal_id=id).all()
        for health in animal_health_to_delete:
            db.session.delete(health)

        # Delete associated data from AnimalOwner
        animal_owner_to_delete = AnimalOwner.query.filter_by(animal_id=id).all()
        for owner in animal_owner_to_delete:
            db.session.delete(owner)

        # Delete associated data from AnimalStory
        animal_story_to_delete = AnimalStory.query.filter_by(animal_id=id).all()
        for story in animal_story_to_delete:
            db.session.delete(story)

        # Finally, delete the Animal record
        db.session.delete(animal)
        db.session.commit()

        flash('Animal and associated data deleted successfully', 'success')
        return redirect(url_for('admin.show_animals'))
    except Exception as e:
        # Log the error to the console or a log file
        print(f"Error deleting animal with ID {id}: {str(e)}")
        flash('An error occurred while deleting the animal', 'error')
        return redirect(url_for('admin.show_animals'))
    
def generate_pdf_with_retry(html_template, retries=3):
    for attempt in range(retries):
        try:
            # Attempt the PDF generation
            pdf_data = pdfkit.from_string(html_template, False, configuration=pdfkit_config ,options={"enable-local-file-access": ""})
            return pdf_data  # If successful, return the PDF data
        except Exception as e:
            # Handle the exception (e.g., log it)
            app.logger.error(f"Attempt {attempt + 1} failed: {str(e)}")

    # If all attempts fail, raise an exception or return an error message
    raise Exception("Failed to generate PDF after multiple attempts")

@animal_blueprint.route('/animal/report/<int:id>', methods=['GET'])
def generate_animal_report(id):
    try:
        animal = Animal.query.get_or_404(id)

        # Access related data
        animal_details = animal.details
        animal_health = animal.health
        animal_owner = animal.owner
        animal_story = animal.story

        if not (animal_details or animal_health or animal_owner or animal_story):
            flash('No data found for this animal.', 'error')
            return redirect(url_for('admin.show_animals'))

        # Render the data into an HTML template]
        html_template = render_template('animal_report.html', animal=animal, animal_details=animal_details,
                                        animal_health=animal_health, animal_owners=animal_owner,
                                        animal_stories=animal_story)

        # Generate PDF using retry logic
        pdf_data = generate_pdf_with_retry(html_template)

        # Return the PDF file as a response without saving it on the server
        response = make_response(pdf_data)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f'inline; filename=animal_report_{id}.pdf'

        return response
    except Exception as e:
        # More detailed error handling
        error_message = f"Error generating the animal report for ID {id}: {str(e)}"
        app.logger.error(error_message)

        # Flash and log the error message
        flash('An error occurred while generating the report. Please check the logs for more details.', 'error')

        # Redirect to the appropriate page
        return redirect(url_for('admin.show_animals'))


@animal_blueprint.route('/add_animal', methods=['GET', 'POST'])
def add_animal():
    if 'username' in session:
        return render_template('add_animal.html')  # Pass the 'form' variable to the template
    else:
        return redirect(url_for('auth.login'))




@animal_blueprint.route('/edit_animal', methods=['GET', 'POST'])
def edit_animal():
    if 'username' in session:
        return render_template('edit_animal.html')  # Pass the 'form' variable to the template
    else:
        return redirect(url_for('auth.login'))
