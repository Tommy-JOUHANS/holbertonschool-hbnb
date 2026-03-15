"""
hbnb/app/models/amenity.py
"""
import uuid
from datetime import datetime
 
from hbnb.app import db
from hbnb.app.models.base_model import BaseModel
 
 
class Amenity(BaseModel, db.Model):
    """Équipement/service disponible dans un logement."""
    __tablename__ = "amenities"
 
    __table_args__ = {"extend_existing": True}
 
    id   = db.Column(db.String(36), primary_key=True,
                     default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(255), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow,
                           nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow,
                           onupdate=datetime.utcnow, nullable=False)
 
    # -------------------------------------------------------------------------
    # Relation Many-to-Many avec Place (via table place_amenity)
    # secondary référencé par nom de table → pas d'import circulaire
    # -------------------------------------------------------------------------
    places = db.relationship(
        'Place',
        secondary='place_amenity',
        back_populates='amenities',
        lazy='select',
    )
 
    # -------------------------------------------------------------------------
    # Constructeur
    # -------------------------------------------------------------------------
    def __init__(self, name, **kwargs):
        super().__init__(**kwargs)
 
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Amenity name is required")
        if len(name) > 255:
            raise ValueError("Amenity name must not exceed 255 characters")
 
        self.name = name
 
    # -------------------------------------------------------------------------
    # Méthodes publiques
    # -------------------------------------------------------------------------
    def to_dict(self) -> dict:
        return {
            'id':         self.id,
            'name':       self.name,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
 
    def update(self, data: dict):
        if 'name' in data:
            if not isinstance(data['name'], str) or not data['name'].strip():
                raise ValueError("Amenity name is required")
            if len(data['name']) > 255:
                raise ValueError("Amenity name must not exceed 255 characters")
            self.name = data['name']
        self.save()
 
    def __repr__(self):
        return f'<Amenity {self.name}>'
    