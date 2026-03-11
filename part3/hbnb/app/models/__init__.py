"""
Models initialization.
"""
from hbnb.app import db

# =========================================================================
# TABLE D'ASSOCIATION Many-to-Many Place <-> Amenity
# Doit être définie AVANT les imports des modèles
# =========================================================================
place_amenity = db.Table(
    'place_amenity',
    db.Column('place_id', db.String(36), db.ForeignKey('places.id', ondelete='CASCADE'), primary_key=True),
    db.Column('amenity_id', db.String(36), db.ForeignKey('amenities.id', ondelete='CASCADE'), primary_key=True)
)

# =========================================================================
# IMPORTS dans le bon ordre
# =========================================================================
from hbnb.app.models.user import User
from hbnb.app.models.amenity import Amenity
from hbnb.app.models.place import Place
from hbnb.app.models.review import Review

__all__ = [
    'User',
    'Place',
    'Review',
    'Amenity',
    'place_amenity',
    'db'
]
