# app_factory.py
from flask import Blueprint
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tails_of_freedom.db'
app.config['UPLOAD_FOLDER']='static/uploaded_images'
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
migrate = Migrate(app,db)

oauth = OAuth(app)
oauth_blueprint = Blueprint('oauth', __name__)



google = oauth.register(
    name='google',
    client_id='529902279308-i6fm3n9si5u233hkrarpv9ufe2l3u41i.apps.googleusercontent.com',
    client_secret='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',
    authorize_params=None,
    access_token_params=None,  # Add any necessary parameters here
    client_kwargs={
        'scope': 'openid email profile',
    },
    server_metadata_url= 'https://accounts.google.com/.well-known/openid-configuration'
)

