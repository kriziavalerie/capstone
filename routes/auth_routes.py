from flask import render_template, request, flash, redirect, url_for, session,Blueprint
from app_factory import db, bcrypt
from models.Admin import Admin
from models.Client import Client



auth_blueprint = Blueprint('auth', __name__)


@auth_blueprint.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('admin.admin_dashboard'))
    return render_template('login.html')




# Logout Route
@auth_blueprint.route('/logout')
def logout():
    session.pop('username', None)  # Remove the 'username' from the session
    session.pop('user_id', None)  # Remove the 'username' from the session
    session.pop('avatar',None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('auth.login'))


@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Store the other form values for preservation
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']

        error_messages = []  # Collect error messages

        if password != confirm_password:
            error_messages.append('Passwords do not match. Please try again.')

        # Check if the username already exists
        existing_username = db.session.query(Client).filter_by(username=username).first()
        if existing_username:
            error_messages.append('Username already exists. Please choose a different username.')

        # Check if the email already exists
        existing_email = db.session.query(Client).filter_by(email=email).first()
        if existing_email:
            error_messages.append('Email is already registered. Please use a different email address.')

        if error_messages:
            # Create a dictionary to store the form values for preservation
            form_values = {
                'username': username,
                'firstname': firstname,
                'lastname': lastname,
                'email': email,
                
            }
            for message in error_messages:
                flash(message, 'danger')
            return render_template('login.html', form_values=form_values)

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        user = Client(username=username, password=hashed_password, first_name=firstname, last_name=lastname, email=email,image_path = "/imageplaceholder.jfif")

        db.session.add(user)
        db.session.commit()
        flash('Your client account has been created!', 'success')
        return render_template('login.html')

        
    return render_template('register.html')

@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Try to find the user in the Admin table first
        admin = Admin.query.filter_by(username=username).first()

        if admin:
            # If an admin is found, check their password
            if bcrypt.check_password_hash(admin.password, password):
                session['user_id'] = admin.id  # Store user ID in session
                session['username'] = username  # Store username in session
                flash('Admin login successful!', 'success')
                return redirect(url_for('admin.admin_dashboard'))
            else:
                flash('Admin login failed. Password is incorrect.', 'danger')
        else:
            # If the username is not found in the Admin table, check the Client table
            client = Client.query.filter_by(username=username).first()

            if client:
                # If a client is found, check their password
                if bcrypt.check_password_hash(client.password, password):
                    session['user_id'] = client.id  # Store user ID in session
                    session['username'] = username  # Store username in session
                    flash('Client login successful!', 'success')
                    return redirect(url_for('client.client_dashboard'))
                else:
                    flash('Client login failed. Password is incorrect.', 'danger')
            else:
                flash('Login failed. User not found.', 'danger')

    return render_template('login.html')
