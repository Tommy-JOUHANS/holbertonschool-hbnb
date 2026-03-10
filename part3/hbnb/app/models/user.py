"""
User model.
Represents a user in the system.
"""
from datetime import datetime
import uuid
import re
from hbnb.app.models.base_model import BaseModel
from hbnb.app import db
from hbnb.app.utils import check_password


class User(BaseModel, db.Model):
    """User model mapped with SQLAlchemy"""
    __tablename__ = "users"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow,
                           onupdate=datetime.utcnow, nullable=False)

    # =========================================================================
    # RELATIONS
    # =========================================================================

    places = db.relationship(
        'Place',
        back_populates='owner',
        cascade='all, delete-orphan',
        lazy='select',
        foreign_keys='Place.owner_id'
    )

    reviews = db.relationship(
        'Review',
        back_populates='user',
        cascade='all, delete-orphan',
        lazy='select',
        foreign_keys='Review.user_id'
    )

    def __init__(self, first_name, last_name, email, password, is_admin=False, **kwargs):
        super().__init__(**kwargs)

        # =====================================================================
        # VALIDATIONS first_name
        # =====================================================================
        if not isinstance(first_name, str) or not first_name.strip():
            raise ValueError("First name is required")
        if len(first_name) > 50:
            raise ValueError("First name must not exceed 50 characters")

        # =====================================================================
        # VALIDATIONS last_name
        # =====================================================================
        if not isinstance(last_name, str) or not last_name.strip():
            raise ValueError("Last name is required")
        if len(last_name) > 50:
            raise ValueError("Last name must not exceed 50 characters")

        # =====================================================================
        # VALIDATIONS email
        # =====================================================================
        if not isinstance(email, str) or not email.strip():
            raise ValueError("Email is required")
        if not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
            raise ValueError("Invalid email format")

        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.is_admin = is_admin

    def __repr__(self):
        return f'<User {self.email}>'

    def to_dict(self):
        """Convert user to dictionary, excluding password"""
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'is_admin': self.is_admin,
            'created_at': self.created_at.isoformat() if hasattr(self, 'created_at') else None,
            'updated_at': self.updated_at.isoformat() if hasattr(self, 'updated_at') else None
        }

    def verify_password(self, password):
        return check_password(self.password, password)

    def update(self, data):
        """Update user attributes with validations"""
        if 'first_name' in data:
            if not isinstance(data['first_name'], str) or not data['first_name'].strip():
                raise ValueError("First name is required")
            if len(data['first_name']) > 50:
                raise ValueError("First name must not exceed 50 characters")

        if 'last_name' in data:
            if not isinstance(data['last_name'], str) or not data['last_name'].strip():
                raise ValueError("Last name is required")
            if len(data['last_name']) > 50:
                raise ValueError("Last name must not exceed 50 characters")

        for key, value in data.items():
            if hasattr(self, key) and key != 'id':
                setattr(self, key, value)
