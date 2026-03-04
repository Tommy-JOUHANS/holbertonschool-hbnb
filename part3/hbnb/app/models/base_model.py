"""
Base model providing common attributes and methods
for all entities.
"""

import uuid
from datetime import datetime


class BaseModel:
    """
    Base class for all models.
    Provides:
    - UUID id
    - created_at
    - updated_at
    """

    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def save(self):
        """
        Updates modification timestamp.
        """
        self.updated_at = datetime.now()

    def update(self, data):
        """
        Updates object attributes dynamically.
        """
        for key, value in data.items():
            if hasattr(self, key) and key not in {"id", "created_at", "updated_at"}:
                setattr(self, key, value)
        self.save()
