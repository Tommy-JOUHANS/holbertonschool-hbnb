"""
Review entity model.
Supports both object references and id references.
"""

from hbnb.app.models.base_model import BaseModel


class Review(BaseModel):

    def __init__(self, text, rating,
                 user=None, place=None,
                 user_id=None, place_id=None):

        super().__init__()

        if not isinstance(text, str) or not text.strip():
            raise ValueError("Review text cannot be empty")

        if not isinstance(rating, int) or not (1 <= rating <= 5):
            raise ValueError("Rating must be an integer between 1 and 5")

        self.text = text
        self.rating = rating

        # 🔥 Support tests (objects)
        if user and place:
            self.user = user
            self.place = place
            self.user_id = user.id
            self.place_id = place.id

        # 🔥 Support API (ids only)
        elif user_id and place_id:
            self.user = None
            self.place = None
            self.user_id = user_id
            self.place_id = place_id

        else:
            raise ValueError("User and Place or user_id and place_id required")

    def to_dict(self):
        return {
            "id": self.id,
            "text": self.text,
            "rating": self.rating,
            "user_id": self.user_id,
            "place_id": self.place_id
        }
