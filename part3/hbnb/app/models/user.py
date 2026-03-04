"""
User model.
Represents a user in the system.
"""
from hbnb.app.models.base_model import BaseModel
import bcrypt


class User(BaseModel):
    def __init__(self, first_name, last_name, email, password, is_admin=False, **kwargs):
        super().__init__(**kwargs)
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password  # Should be hashed before storage
        self.is_admin = is_admin
    
    def to_dict(self):
        """Convert user to dictionary, excluding password"""
        user_dict = super().to_dict()
        user_dict.update({
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'is_admin': self.is_admin
            # Password is intentionally excluded for security
        })
        return user_dict
    
    def verify_password(self, password):
        """
        Verify if the provided password matches the hashed password.
        
        Args:
            password (str): Plain text password to verify
            
        Returns:
            bool: True if password matches, False otherwise
        """
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))
    
    def update(self, data):
        """Update user attributes"""
        for key, value in data.items():
            if hasattr(self, key) and key != 'id':  # Don't allow ID updates
                setattr(self, key, value)
