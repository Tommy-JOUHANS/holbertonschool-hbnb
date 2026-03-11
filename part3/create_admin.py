"""
Script to create an admin user.
Run this once to bootstrap the application with an admin account.
"""
from hbnb.app import create_app
from hbnb.app.services import facade
from hbnb.app.utils import hash_password

app = create_app()

with app.app_context():
    admin_data = {
        "first_name": "Admin",
        "last_name": "User",
        "email": "admin@hbnb.com",
        "password": hash_password("admin123"),
        "is_admin": True
    }
    
    try:
        admin = facade.create_user(admin_data)
        print(f"✓ Admin user created successfully!")
        print(f"  Email: admin@hbnb.com")
        print(f"  Password: admin123")
        print(f"  ID: {admin.id}")
    except ValueError as e:
        print(f"✗ Error: {e}")
        print("Admin user may already exist.")
