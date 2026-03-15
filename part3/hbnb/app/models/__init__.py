"""
hbnb/app/models/__init__.py
 
Critical import order:

1. db (from hbnb.app — already initialized when you arrive here)

2. Place_amenity association table (referenced by Place and Amenity)

3. BaseModel

4. User, Amenity, Place, Review (in this order for foreign keys)

Never import namespaces or services here → circular import.
"""
from hbnb.app import db
 
# =============================================================================
# Many-to-Many Place <-> Amenity MATCHING TABLE
# Defined BEFORE the models that use it via secondary='place_amenity'
# =============================================================================
place_amenity = db.Table(
    'place_amenity',
    db.Column(
        'place_id',
        db.String(36),
        db.ForeignKey('places.id', ondelete='CASCADE'),
        primary_key=True,
    ),
    db.Column(
        'amenity_id',
        db.String(36),
        db.ForeignKey('amenities.id', ondelete='CASCADE'),
        primary_key=True,
    ),
    # Avoids "Table already defined" if create_app() is called multiple times
    # (unit tests)
    extend_existing=True,
)
 
# =============================================================================
# IMPORTS of models
# =============================================================================
from hbnb.app.models.user import User          # noqa: E402, F401
from hbnb.app.models.amenity import Amenity    # noqa: E402, F401
from hbnb.app.models.place import Place        # noqa: E402, F401
from hbnb.app.models.review import Review      # noqa: E402, F401
 
__all__ = [
    'db',
    'place_amenity',
    'User',
    'Amenity',
    'Place',
    'Review',
]