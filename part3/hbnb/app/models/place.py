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

    def __init__(self, title, description, price, latitude, longitude, owner_id, **kwargs):
        super().__init__(**kwargs)

        # =====================================================================
        # VALIDATIONS title
        # =====================================================================
        if not isinstance(title, str) or not title.strip():
            raise ValueError("Title is required")
        if len(title) > 255:
            raise ValueError("Title must not exceed 255 characters")

        # =====================================================================
        # VALIDATIONS description
        # =====================================================================
        if description is not None and len(description) > 1000:
            raise ValueError("Description must not exceed 1000 characters")

        # =====================================================================
        # VALIDATIONS price
        # =====================================================================
        if not isinstance(price, (int, float)) or price < 0:
            raise ValueError("Price must be a positive number")

        # =====================================================================
        # VALIDATIONS latitude / longitude
        # =====================================================================
        if not isinstance(latitude, (int, float)) or not (-90 <= latitude <= 90):
            raise ValueError("Latitude must be between -90 and 90")
        if not isinstance(longitude, (int, float)) or not (-180 <= longitude <= 180):
            raise ValueError("Longitude must be between -180 and 180")

        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id


    def __repr__(self):
        return f'<Place {self.title}>'

    def to_dict(self, include_owner=False, include_reviews=False, include_amenities=False):
        data = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'owner_id': self.owner_id,
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
        """Update place attributes with validations"""
        if 'title' in data:
            if not isinstance(data['title'], str) or not data['title'].strip():
                raise ValueError("Title is required")
            if len(data['title']) > 255:
                raise ValueError("Title must not exceed 255 characters")

        if 'description' in data and data['description'] is not None:
            if len(data['description']) > 1000:
                raise ValueError("Description must not exceed 1000 characters")

        if 'price' in data:
            if not isinstance(data['price'], (int, float)) or data['price'] < 0:
                raise ValueError("Price must be a positive number")

        if 'latitude' in data:
            if not (-90 <= data['latitude'] <= 90):
                raise ValueError("Latitude must be between -90 and 90")

        if 'longitude' in data:
            if not (-180 <= data['longitude'] <= 180):
                raise ValueError("Longitude must be between -180 and 180")

        allowed_fields = [
            'title', 'description', 'price', 'latitude', 'longitude'
        ]
        for key, value in data.items():
            if hasattr(self, key) and key in allowed_fields:
                setattr(self, key, value)

