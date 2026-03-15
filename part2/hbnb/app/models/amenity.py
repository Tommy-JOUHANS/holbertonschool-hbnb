"""
Amenity entity model.
"""


from hbnb.app.models.base_model import BaseModel


class Amenity(BaseModel):

    def __init__(self, name, description=None):
        super().__init__()

        if not isinstance(name, str) or not name.strip():
            raise ValueError("Amenity name is required")
        if len(name) > 255:
            raise ValueError("Amenity name must not exceed 255 characters")

        self.name = name


    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,

        }
