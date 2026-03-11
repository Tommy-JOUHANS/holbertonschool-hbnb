"""
Place_Amenity association table.
Represents the many-to-many relationship between Place and Amenity.
"""
from hbnb.app import db


# =========================================================================
# TABLE D'ASSOCIATION POUR LA RELATION MANY-TO-MANY
# =========================================================================

place_amenity = db.Table(
    'place_amenity',
    db.Column('place_id', db.String(36), 
              db.ForeignKey('places.id', ondelete='CASCADE'), 
              primary_key=True),
    db.Column('amenity_id', db.String(36), 
              db.ForeignKey('amenities.id', ondelete='CASCADE'), 
              primary_key=True)
)

"""
Cette table d'association crée une relation many-to-many entre Place et Amenity.

Utilisation dans les modèles:
- Place: 
    amenities = db.relationship(
        'Amenity',
        secondary='place_amenity',
        back_populates='places',
        lazy='select'
    )

- Amenity:
    places = db.relationship(
        'Place',
        secondary='place_amenity',
        back_populates='amenities',
        lazy='select'
    )

Les deux colonnes (place_id, amenity_id) forment une clé composite primaire.
"""
