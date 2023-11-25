# config.py

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate

app_config = {
    'SESSION_TYPE': 'filesystem',
    'SQLALCHEMY_DATABASE_URI': 'sqlite:///tails_of_freedom.db',
    'UPLOAD_FOLDER': 'static/uploaded_images',
    'SECRET_KEY': 'your_secret_key',
}

db = SQLAlchemy()
bcrypt = Bcrypt()
migrate = Migrate()
