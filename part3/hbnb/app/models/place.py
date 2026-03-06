"""
Place entity model.
Supports both owner object and owner_id.
"""

from hbnb.app.models.base_model import BaseModel
from hbnb.app import db
import uuid


class Place(BaseModel, db.Model):
    """Place model mapped with SQLAlchemy"""
    __tablename__ = "places"

    # ✅ Utilisation d'un UUID comme clé primaire
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(1024), nullable=True)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    def __init__(self, title, description, price, latitude, longitude,
                 owner=None, owner_id=None):

        super().__init__()

        if not isinstance(title, str) or not title.strip():
            raise ValueError("Title is required")

        if not isinstance(price, (int, float)) or price < 0:
            raise TypeError("Price must be a number")

        if not isinstance(latitude, (int, float)) or not (-90 <= latitude <= 90):
            raise ValueError("Latitude must be between -90 and 90")

        if not isinstance(longitude, (int, float)) or not (-180 <= longitude <= 180):
            raise ValueError("Longitude must be between -180 and 180")

        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude

        # support both test and API usage
        if owner:
            self.owner = owner
            self.owner_id = owner.id
        elif owner_id:
            self.owner = None
            self.owner_id = owner_id
        else:
            raise ValueError("Owner or owner_id is required")

        self.amenities = []
        self.reviews = []

    def add_review(self, review):
        """Adds a review to the place."""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Adds amenities to the place."""
        if amenity not in self.amenities:
            self.amenities.append(amenity)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "owner_id": getattr(self, "owner_id", None),
            "amenities": [a.to_dict() for a in self.amenities],
            "reviews": [r.to_dict() for r in self.reviews]
        }
