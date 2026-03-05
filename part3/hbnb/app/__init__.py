from flask import Flask
from flask_restx import Api
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from hbnb.app.config import Config, DevelopmentConfig
from flask_sqlalchemy import SQLAlchemy
from hbnb.app.api.v1.users import api as users_ns
from hbnb.app.api.v1.places import api as places_ns
from hbnb.app.api.v1.reviews import api as reviews_ns
from hbnb.app.api.v1.amenities import api as amenities_ns
from hbnb.app.api.v1.auth import api as auth_ns

# Initialisations globales
jwt = JWTManager()
bcrypt = Bcrypt()
db = SQLAlchemy()  # <-- ajout de SQLAlchemy

def create_app(config_class=None):
    """Create and configure the Flask application.
    
    Args:
        config_class: Flask configuration class. Defaults to DevelopmentConfig.
    """
    if config_class is None:
        config_class = DevelopmentConfig
    
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Routes simples
    @app.route("/")
    def home():
        return "Welcome to the HBnB API! Visit /api/v1/ for documentation."
    
    # Initialisations
    jwt.init_app(app)
    bcrypt.init_app(app)
    db.init_app(app)  # <-- initialisation SQLAlchemy
    
    # API REST
    api = Api(app, title="HBnB API", version="1.0", doc="/api/v1/docs")
    api.add_namespace(users_ns, path="/api/v1/users")
    api.add_namespace(places_ns, path="/api/v1/places")
    api.add_namespace(reviews_ns, path="/api/v1/reviews")
    api.add_namespace(amenities_ns, path="/api/v1/amenities")
    api.add_namespace(auth_ns, path="/api/v1/auth")
    
    return app
