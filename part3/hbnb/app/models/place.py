"""
Place entity model.
Supports both owner object and owner_id.
"""

from hbnb.app.models.base_model import BaseModel


class Place(BaseModel):

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

        # 🔥 support both test and API usage
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
        """
        Adds a review to the place.
        """
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """
        Adds amenities to the place.
        """
        if amenity not in self.add_amenities:
            self.amenities.append(amenity)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "owner_id": self.owner_id,
            "amenities": [a.to_dict() for a in self.amenities],
            "reviews": [r.to_dict() for r in self.reviews]
        }

