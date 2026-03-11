"""
hbnb/app/__init__.py - Application Factory Pattern
"""
from flask import Flask
from flask_restx import Api
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from hbnb.app.config import DevelopmentConfig

# ✅ INITIALISATIONS GLOBALES - Créer AVANT d'importer les modèles
jwt = JWTManager()
bcrypt = Bcrypt()
db = SQLAlchemy()

def create_app(config_class=None):
    if config_class is None:
        config_class = DevelopmentConfig

    # ========== 1. CRÉER L'APP ==========
    app = Flask(__name__)
    app.config.from_object(config_class)

    # ========== 2. INITIALISER LES EXTENSIONS ==========
    jwt.init_app(app)
    bcrypt.init_app(app)
    db.init_app(app)

    # ========== 3. ROUTE DE BASE ==========
    @app.route("/")
    def home():
        return "Welcome to the HBnB API! Visit /api/v1/ for documentation."

    # ========== 4. ENREGISTRER LES NAMESPACES API ==========
    # ⚠️ Ces imports chargent les modèles SQLAlchemy en mémoire
    from hbnb.app.api.v1.users import api as users_ns
    from hbnb.app.api.v1.places import api as places_ns
    from hbnb.app.api.v1.reviews import api as reviews_ns
    from hbnb.app.api.v1.amenities import api as amenities_ns
    from hbnb.app.api.v1.auth import api as auth_ns

    api = Api(app, title="HBnB API", version="1.0", doc="/api/v1/docs")
    api.add_namespace(users_ns, path="/api/v1/users")
    api.add_namespace(places_ns, path="/api/v1/places")
    api.add_namespace(reviews_ns, path="/api/v1/reviews")
    api.add_namespace(amenities_ns, path="/api/v1/amenities")
    api.add_namespace(auth_ns, path="/api/v1/auth")

    # ========== 5. CRÉER LES TABLES ==========
    # ✅ APRÈS les imports des namespaces, SQLAlchemy connaît tous les modèles
    with app.app_context():
        from hbnb.app.models import User, Place, Review, Amenity
        db.create_all()

    # ========== 6. INITIALISER LES DONNÉES ==========
    with app.app_context():
        try:
            from hbnb.app.services import facade
            from hbnb.app.utils import hash_password

            existing_admin = facade.get_user_by_email("admin@example.com")

            if not existing_admin:
                try:
                    admin_data = {
                        "first_name": "Admin",
                        "last_name": "User",
                        "email": "admin@example.com",
                        "password": hash_password("admin123"),
                        "is_admin": True
                    }
                    admin = facade.create_user(admin_data)
                    print(f"✅ Admin user initialized with ID: {admin.id}")
                except Exception as e:
                    print(f"⚠️  Could not initialize admin user: {e}")
            else:
                print("✅ Admin user already exists")
        except Exception as e:
            print(f"⚠️  Could not initialize database: {e}")

    return app
