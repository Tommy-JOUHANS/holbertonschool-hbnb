"""
Models initialization.
Initializes all models and associations for the HBnB application.
"""

from hbnb.app import db

# =========================================================================
# IMPORTANT: Importer dans le bon ordre pour éviter les erreurs
# =========================================================================

# 1. D'abord importer User et Amenity (sans dépendances circulaires)
from hbnb.app.models.user import User
from hbnb.app.models.amenity import Amenity

# 2. Ensuite importer Place (qui utilise place_amenity)
from hbnb.app.models.place import Place, place_amenity

# 3. Enfin importer Review (qui dépend de User et Place)
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
