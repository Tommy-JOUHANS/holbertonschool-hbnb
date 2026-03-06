"""
Amenity entity model.
"""

from hbnb.app.models.base_model import BaseModel
from hbnb.app import db
import uuid


class Amenity(BaseModel, db.Model):
    """Amenity model mapped with SQLAlchemy"""
    __tablename__ = "amenities"

    # ✅ UUID pour l'ID
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(1024), nullable=True)

    def __init__(self, name, description=None):
        super().__init__()

        if not isinstance(name, str) or not name.strip():
            raise ValueError("Amenity name is required")

        self.name = name
        self.description = description

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description
        }
