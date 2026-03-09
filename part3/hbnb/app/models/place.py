"""
Place model.
Represents a place/accommodation in the system.
"""
from datetime import datetime
import uuid
from hbnb.app.models.base_model import BaseModel
from hbnb.app import db

class Place(BaseModel, db.Model):
    """Place model mapped with SQLAlchemy"""
    __tablename__ = "places"
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    owner_id = db.Column(db.String(36), db.ForeignKey('users.id', ondelete='CASCADE'), 
                        nullable=False)
    number_rooms = db.Column(db.Integer, default=0)
    number_bathrooms = db.Column(db.Integer, default=0)
    max_guest = db.Column(db.Integer, default=0)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, 
                          onupdate=datetime.utcnow, nullable=False)
    
    # =========================================================================
    # RELATIONS
    # =========================================================================
    
    owner = db.relationship(
        'User',
        back_populates='places',
        lazy='select',
        foreign_keys=[owner_id]
    )
    
    reviews = db.relationship(
        'Review',
        back_populates='place',
        cascade='all, delete-orphan',
        lazy='select',
        foreign_keys='Review.place_id'
    )

    amenities = db.relationship(
        'Amenity',
        secondary='place_amenity',
        back_populates='places',
        lazy='select'
    )
    
    def __init__(self, title, description, price, latitude, longitude, owner_id,
                 number_rooms=0, number_bathrooms=0, max_guest=0, **kwargs):
        """
        Initialize Place with required fields.
        
        Args:
            title (str): Title of the place
            description (str): Description of the place
            price (float): Price per night
            latitude (float): Latitude coordinate
            longitude (float): Longitude coordinate
            owner_id (str): ID of the owner (User)
            number_rooms (int): Number of rooms
            number_bathrooms (int): Number of bathrooms
            max_guest (int): Maximum number of guests
        """
        super().__init__(**kwargs)
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id
        self.number_rooms = number_rooms
        self.number_bathrooms = number_bathrooms
        self.max_guest = max_guest
    
    def __repr__(self):
        return f'<Place {self.title}>'
    
    def to_dict(self, include_owner=False, include_reviews=False, include_amenities=False):
        """
        Convert place to dictionary.
        
        Args:
            include_owner (bool): Inclure les détails du propriétaire
            include_reviews (bool): Inclure la liste des reviews
            include_amenities (bool): Inclure la liste des amenities
        """
        data = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'owner_id': self.owner_id,
            'number_rooms': self.number_rooms,
            'number_bathrooms': self.number_bathrooms,
            'max_guest': self.max_guest,
            'created_at': self.created_at.isoformat() if hasattr(self, 'created_at') else None,
            'updated_at': self.updated_at.isoformat() if hasattr(self, 'updated_at') else None
        }
        
        if include_owner and self.owner:
            data['owner'] = self.owner.to_dict()
        
        if include_reviews and self.reviews:
            data['reviews'] = [review.to_dict() for review in self.reviews]
        
        if include_amenities and self.amenities:
            data['amenities'] = [amenity.to_dict() for amenity in self.amenities]
        
        return data
    
    def update(self, data):
        """Update place attributes"""
        allowed_fields = [
            'title', 'description', 'price', 'latitude', 'longitude',
            'number_rooms', 'number_bathrooms', 'max_guest'
        ]
        
        for key, value in data.items():
            if hasattr(self, key) and key in allowed_fields and key != 'id':
                setattr(self, key, value)
