from flask import Flask
from os import path
import os

DB_NAME = "database.db"
UPLOAD_FOLDER = 'uploads'

#initializes and configures the flask application
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'this_is_a_very_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
   
    base_dir = os.path.abspath(os.path.dirname(__file__))
    app.config['UPLOAD_FOLDER'] = os.path.join(base_dir, UPLOAD_FOLDER)
    
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    from .models import db
    db.init_app(app)

    from .views import views
    from .mods import mods

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(mods, url_prefix='/mods')  

    create_database(app)

    return app
#checks if the database exists and creates it if not.
def create_database(app):
    if not path.exists('website/' + DB_NAME):
        with app.app_context():
            from .models import db
            db.create_all()
            print('Database Created Successfully!')