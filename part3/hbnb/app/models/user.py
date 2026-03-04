"""
User model.
Represents a user in the system.
"""
from hbnb.app.models.base_model import BaseModel


class User(BaseModel):
    def __init__(self, first_name, last_name, email, password, **kwargs):
        super().__init__(**kwargs)
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password  # ✅ Ajoutez cette ligne
    
    def to_dict(self):
        """Convert user to dictionary, excluding password"""
        user_dict = super().to_dict()
        user_dict.update({
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email
            # Password is intentionally excluded for security
        })
        return user_dict
    
    def update(self, data):
        """Update user attributes"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
