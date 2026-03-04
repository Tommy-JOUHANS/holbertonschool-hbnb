"""
Application factory for HBnB API.
Initializes Flask app and registers all namespaces.
"""
from flask import Flask
from flask_restx import Api
from flask_bcrypt import Bcrypt
from hbnb.app.api.v1.users import api as users_ns
from hbnb.app.api.v1.places import api as places_ns
from hbnb.app.api.v1.amenities import api as amenities_ns
from hbnb.app.api.v1.reviews import api as reviews_ns

bcrypt = Bcrypt()


def create_app(config_class=None):
    """
    Creates and configures the Flask application.
    
    Args:
        config_class: Configuration class to use (default: DevelopmentConfig)
    
    Returns:
        Flask application instance
    """
    app = Flask(__name__)
    
    # Import config here to avoid circular import
    if config_class is None:
        from hbnb.app.config import DevelopmentConfig
        config_class = DevelopmentConfig
    
    app.config.from_object(config_class)
    
    # Initialize extensions
    bcrypt.init_app(app)
    
    # Define routes
    @app.route("/")
    def home():
        return "Welcome to the HBnB API! Visit /api/v1/ for documentation."
    
    # Initialize API
    api = Api(
        app,
        version="1.0",
        title="HBnB API",
        description="HBnB Application REST API",
        doc="/api/v1/"
    )
    
    # Register namespaces
    api.add_namespace(users_ns, path="/api/v1/users")
    api.add_namespace(places_ns, path="/api/v1/places")
    api.add_namespace(amenities_ns, path="/api/v1/amenities")
    api.add_namespace(reviews_ns, path="/api/v1/reviews")
    
    return app
