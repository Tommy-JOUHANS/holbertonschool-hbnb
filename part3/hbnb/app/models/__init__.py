"""
Models initialization.
Initializes all models and associations for the HBnB application.
"""
from hbnb.app import db

# =========================================================================
# TABLE D'ASSOCIATION place_amenity (Many-to-Many)
# =========================================================================
place_amenity = db.Table(
    'place_amenity',
    db.Column('place_id', db.String(36), db.ForeignKey('places.id', ondelete='CASCADE'), primary_key=True),
    db.Column('amenity_id', db.String(36), db.ForeignKey('amenities.id', ondelete='CASCADE'), primary_key=True)
)

# =========================================================================
# IMPORTANT: Importer dans le bon ordre pour éviter les erreurs circulaires
# =========================================================================
# 1. D'abord User et Amenity (sans dépendances circulaires)
from hbnb.app.models.user import User
from hbnb.app.models.amenity import Amenity
# 2. Ensuite Place (qui utilise place_amenity)
from hbnb.app.models.place import Place
# 3. Enfin Review (qui dépend de User et Place)
from hbnb.app.models.review import Review

# =========================================================================
# EXPORTER POUR UTILISATION
# =========================================================================
__all__ = [
    'User',
    'Place',
    'Review',
    'Amenity',
    'place_amenity',
    'db'
]
