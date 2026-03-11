"""SQLAlchemy repository implementation.
This module provides a concrete implementation of the Repository interface
using SQLAlchemy for database persistence.
"""
from hbnb.app import db
from hbnb.app.persistence.repository import Repository

class SQLAlchemyRepository(Repository):
    """SQLAlchemy-based repository implementation.
    
    This repository provides CRUD operations for any SQLAlchemy model,
    making it reusable across different entities (User, Place, Review, etc.).
    
    Attributes:
        model: The SQLAlchemy model class this repository manages
    """
    def __init__(self, model):
        """Initialize the repository with a specific SQLAlchemy model.
        
        Args:
            model: The SQLAlchemy model class to manage
        """
        self.model = model
    
    def add(self, obj):
        """Add a new object to the database.
        
        Args:
            obj: The model instance to add
            
        Note:
            This method commits the transaction immediately.
        """
        db.session.add(obj)
        db.session.commit()
    
    def get(self, obj_id):
        """Retrieve an object by its ID.
        
        Args:
            obj_id: The ID of the object to retrieve
            
        Returns:
            The object if found, None otherwise
        """
        return self.model.query.get(obj_id)
    
    def get_all(self):
        """Retrieve all objects of this model type.
        
        Returns:
            list: List of all objects
        """
        return self.model.query.all()
    
    def update(self, obj_id, data):
        """Update an object with new data.
        
        Args:
            obj_id: The ID of the object to update
            data (dict): Dictionary containing the fields to update
            
        Note:
            This method commits the transaction immediately if the object exists.
        """
        obj = self.get(obj_id)
        if obj:
            for key, value in data.items():
                setattr(obj, key, value)
            db.session.commit()
    
    def delete(self, obj_id):
        """Delete an object by its ID.
        
        Args:
            obj_id: The ID of the object to delete
            
        Note:
            This method commits the transaction immediately if the object exists.
        """
        obj = self.get(obj_id)
        if obj:
            db.session.delete(obj)
            db.session.commit()
    
    def get_by_attribute(self, attr_name, attr_value):
        """Retrieve an object by a specific attribute.
        
        Args:
            attr_name (str): The name of the attribute to filter by
            attr_value: The value to search for
            
        Returns:
            The first object matching the criteria, None otherwise
            
        Example:
            repository.get_by_attribute('email', 'user@example.com')
        """
        return self.model.query.filter_by(**{attr_name: attr_value}).first()
