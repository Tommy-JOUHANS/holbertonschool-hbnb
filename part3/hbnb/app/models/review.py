"""
Review model.
Represents a review/rating for a place.
"""
from datetime import datetime
import uuid
from hbnb.app.models.base_model import BaseModel
from hbnb.app import db


class Review(BaseModel, db.Model):
    """Review model mapped with SQLAlchemy"""
    __tablename__ = "reviews"
    
    # ✅ UUID pour l'ID
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id', ondelete='CASCADE'), 
                       nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey('places.id', ondelete='CASCADE'), 
                        nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, 
                          onupdate=datetime.utcnow, nullable=False)
    
    # =========================================================================
    # CONTRAINTES
    # =========================================================================
    
    __table_args__ = (
        db.UniqueConstraint('user_id', 'place_id', name='uq_user_place_review'),
        db.CheckConstraint('rating >= 1 AND rating <= 5', name='ck_review_rating'),
    )
    
    # =========================================================================
    # RELATIONS
    # =========================================================================
    
    # Many-to-One: Une review est écrite par un utilisateur
    user = db.relationship(
        'User',
        back_populates='reviews',
        lazy='select',
        foreign_keys=[user_id]
    )
    
    # Many-to-One: Une review concerne une place
    place = db.relationship(
        'Place',
        back_populates='reviews',
        lazy='select',
        foreign_keys=[place_id]
    )
    
    def __init__(self, text, rating, user_id, place_id, **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.rating = rating
        self.user_id = user_id
        self.place_id = place_id
    
    def __repr__(self):
        return f'<Review {self.rating}★ for place {self.place_id}>'
    
    def to_dict(self, include_user=False, include_place=False):
        """
        Convert review to dictionary
        
        Args:
            include_user: Include user details
            include_place: Include place details
        """
        data = {
            'id': self.id,
            'text': self.text,
            'rating': self.rating,
            'user_id': self.user_id,
            'place_id': self.place_id,
            'created_at': self.created_at.isoformat() if hasattr(self, 'created_at') else None,
            'updated_at': self.updated_at.isoformat() if hasattr(self, 'updated_at') else None
        }
        
        if include_user and self.user:
            data['user'] = self.user.to_dict()
        
        if include_place and self.place:
            data['place'] = self.place.to_dict()
        
        return data
    
    def update(self, data):
        """Update review attributes"""
        for key, value in data.items():
            if hasattr(self, key) and key not in ['id', 'user_id', 'place_id']:
                setattr(self, key, value)
