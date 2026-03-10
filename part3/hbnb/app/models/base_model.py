"""
Base model providing common attributes and methods for all entities.
"""
import uuid
from datetime import datetime
from hbnb.app import db

class BaseModel(db.Model):
    __abstract__ = True  #  SQLAlchemy ne crée pas de table pour BaseModel

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow,
                           onupdate=datetime.utcnow, nullable=False)

    def __init__(self, **kwargs):
        #  Ne pas appeler super().__init__() avec des args positionnels
        if 'id' not in kwargs:
            self.id = str(uuid.uuid4())
        if 'created_at' not in kwargs:
            self.created_at = datetime.utcnow()
        if 'updated_at' not in kwargs:
            self.updated_at = datetime.utcnow()

    def save(self):
        self.updated_at = datetime.utcnow()

    def update(self, data):
        for key, value in data.items():
            if hasattr(self, key) and key not in {"id", "created_at"}:
                setattr(self, key, value)
        self.save()