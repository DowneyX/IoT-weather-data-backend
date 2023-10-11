from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import config

db = SQLAlchemy()
DB_NAME = 'database.db'

def create_app():
    """ initialises the website"""

    app = Flask(__name__, template_folder='templates')

    login_manager = LoginManager()
    login_manager.init_app(app)

    # WHEN IN PRODUCTION NEVER SHARE THIS KEY AND CHANGE IT TO SOMETHING THAT MAKES MORE SENSE
    app.config['SECRET_KEY'] = config.SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
    db.init_app(app)

    from .models import WeatherData

    with app.app_context():
        db.create_all()

    from .routes.WeatherApiController import weather_data_api

    app.register_blueprint(weather_data_api, url_prefix='/api/weather_data')
    return app