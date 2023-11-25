from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app_factory import db
from app_factory import app
from models.Client import Client
from app_factory import oauth
from app_factory import google
import secrets
from datetime import datetime




google_oauth_blueprint = Blueprint('google_oauth', __name__)

nonce = secrets.token_hex(16)  # Generates a 32-character hexadecimal nonce
@google_oauth_blueprint.route('/login')
def google_login():
    # Store the nonce in the session
    session['google_nonce'] = nonce

    # Initiate the Google OAuth flow
    return google.authorize_redirect(redirect_uri='http://127.0.0.1:5000/google/authorized', nonce=nonce)

@google_oauth_blueprint.route('/logout')
def google_logout():
    session.pop('google_token', None)
    return redirect(url_for('index'))

# Define the authorized route for Google OAuth
@google_oauth_blueprint.route('/authorized')
def google_authorized():
    token = google.authorize_access_token()

    # Retrieve the nonce from the session
    nonce = session.get('google_nonce')

    if nonce is None:
        # Handle the case where nonce is missing
        return 'Nonce is missing'

    user_info = google.parse_id_token(token, nonce=nonce)

    if user_info is None:
        # Handle the case where the nonce doesn't match
        return 'Nonce verification failed'

    # Extract user information from Google response
    first_name = user_info.get('given_name', '')
    last_name = user_info.get('family_name', '')
    email = user_info.get('email', '')
    username = email  # You can use the email as the username
    avatar = user_info.get('picture')


    # Check if the user already exists in the database
    existing_user = Client.query.filter_by(email=email).first()
    if existing_user:
        # User already exists, you can log them in or do additional actions here
        session['username'] = existing_user.email
        session['user_id'] = existing_user.id
        session['avatar'] = avatar
        flash('Client login successful!', 'success')

        return redirect(url_for('client.client_dashboard'))

    else:
        # User doesn't exist, create a new Client instance and add it to the database
        

        new_client = Client(
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=username,
            image_path = avatar
            # You may need to set other attributes as well
        )

        
        db.session.add(new_client)
        db.session.commit()
        # User already exists, you can log them in or do additional actions here
        session['username'] = new_client.email
        session['user_id'] = new_client.id
        session['avatar'] = avatar
        flash('Client registered successful!', 'success')

        # Now, the user is registered and logged in as a Client
        return redirect(url_for('client.client_dashboard'))