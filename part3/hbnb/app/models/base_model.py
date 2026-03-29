"""
hbnb/app/models/base_model.py
 
Classe abstraite commune à tous les modèles SQLAlchemy.
N'importe QUE db — aucun autre modèle, aucun service.
"""
import uuid
from datetime import datetime
from hbnb.app import db
 
 
class BaseModel(db.Model):
    """Abstract base — SQLAlchemy ne crée pas de table pour cette classe."""
    __abstract__ = True
 
    id = db.Column(
        db.String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )
    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False,
    )
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )
 
    def __init__(self, **kwargs):
        # Ne pas transmettre les kwargs inconnus à db.Model
        super().__init__(**kwargs)
        if not self.id:
            self.id = str(uuid.uuid4())
        if not self.created_at:
            self.created_at = datetime.utcnow()
        if not self.updated_at:
            self.updated_at = datetime.utcnow()
 
    def save(self):
        """Marquer l'objet comme modifié."""
        self.updated_at = datetime.utcnow()
        db.session.add(self) 
 
    def update(self, data: dict):
        """Mise à jour générique (sans validation métier)."""
        for key, value in data.items():
            if hasattr(self, key) and key not in {"id", "created_at"}:
                setattr(self, key, value)
        self.save()