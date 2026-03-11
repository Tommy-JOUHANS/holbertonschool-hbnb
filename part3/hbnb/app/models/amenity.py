"""
Amenity model.
Represents an amenity/service available in a place.
"""
from datetime import datetime
import uuid
from hbnb.app.models.base_model import BaseModel
from hbnb.app import db


class Amenity(BaseModel, db.Model):
    """Amenity model mapped with SQLAlchemy"""
    __tablename__ = "amenities"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(255), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow,
                           onupdate=datetime.utcnow, nullable=False)

    # =========================================================================
    # RELATIONS
    # =========================================================================

    places = db.relationship(
        'Place',
        secondary='place_amenity',
        back_populates='amenities',
        lazy='select'
    )

    def __init__(self, name, **kwargs):
        super().__init__(**kwargs)

        # =====================================================================
        # VALIDATIONS name
        # =====================================================================
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Amenity name is required")
        if len(name) > 255:
            raise ValueError("Amenity name must not exceed 255 characters")

        self.name = name

    def __repr__(self):
        return f'<Amenity {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at.isoformat() if hasattr(self, 'created_at') else None,
            'updated_at': self.updated_at.isoformat() if hasattr(self, 'updated_at') else None
        }

    def update(self, data):
        """Update amenity attributes with validations"""
        if 'name' in data:
            if not isinstance(data['name'], str) or not data['name'].strip():
                raise ValueError("Amenity name is required")
            if len(data['name']) > 255:
                raise ValueError("Amenity name must not exceed 255 characters")

        for key, value in data.items():
            if hasattr(self, key) and key != 'id':
                setattr(self, key, value)
