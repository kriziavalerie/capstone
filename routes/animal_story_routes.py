from flask import Blueprint, render_template, redirect, url_for, request, flash
from app_factory import db
from models.AnimalStory import AnimalStory
from models.Animal import Animal

animal_story_blueprint = Blueprint('animal_story', __name__)
#Animal Story
@animal_story_blueprint.route('/animal/story/create', methods=['POST'])
def create_animal_story():
    # Retrieve form data for creating an AnimalStory
    animal_id = request.form.get('animal_id')
    story = request.form.get('story')
    animal = Animal.query.get(animal_id)

    # Perform basic validation
    if not animal_id or not story:
        flash('Both animal_id and story are required', 'danger')
        return render_template('add_animal.html')  # Render the 'add_animal.html' template with an error message

    # You can add additional validation here if needed
    # For example, you can check if the provided animal_id exists in your database.

    # Create a new AnimalStory object and add it to the database
    animal_story = AnimalStory(animal_id=animal_id, story=story)
    db.session.add(animal_story)
    db.session.commit()

    # Flash a success message and redirect to a relevant page
    flash('Animal story created successfully', 'success')
    return render_template('add_animal.html',
                               animal_id=animal_id, story=story,
                            
                                relative_image_path=animal.image_path
                           )



@animal_story_blueprint.route('/animal/story/edit/<int:animal_id>', methods=['GET', 'POST'])
def edit_animal_story(animal_id):
    # Find the existing animal story by its animal_id
    animal_story = AnimalStory.query.filter_by(animal_id=animal_id).first()
    
    if request.method == 'POST':
        # Retrieve form data for editing or creating an AnimalStory
        story = request.form.get('story')

        # Perform basic validation
        if not story:
            flash('Story is required', 'danger')
        else:
            if animal_story:
                # If the animal_story exists, update it
                animal_story.story = story
                flash('Animal story updated successfully', 'success')
            else:
                # If the animal_story doesn't exist, create a new one
                new_animal_story = AnimalStory(
                    animal_id=animal_id,
                    story=story
                )
                db.session.add(new_animal_story)
                flash('Animal story created successfully', 'success')

            db.session.commit()
            return redirect(url_for('admin.show_animals'))

    # Render the edit template with the existing or a new animal_story
    return render_template('edit_animal.html', animal_story=animal_story, animal_id=animal_id)

