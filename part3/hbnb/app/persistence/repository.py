"""
Repository implementations for data persistence.
Supports both in-memory and SQLAlchemy-based persistence.
"""
from abc import ABC, abstractmethod

# Global storage for InMemoryRepository (persists across instances)
_GLOBAL_STORAGE = {}

class Repository(ABC):
    """Abstract base repository interface"""
    
    @abstractmethod
    def add(self, obj):
        pass
    
    @abstractmethod
    def get(self, obj_id):
        pass
    
    @abstractmethod
    def get_all(self):
        pass
    
    @abstractmethod
    def update(self, obj_id, data):
        pass
    
    @abstractmethod
    def delete(self, obj_id):
        pass
    
    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        pass


class InMemoryRepository(Repository):
    """In-memory repository implementation with global storage"""
    
    def __init__(self):
        """Initialize with global storage"""
        # Use global storage instead of instance storage
        # This ensures data persists across different repository instances
        pass
    
    def add(self, obj):
        """Add object to global storage"""
        _GLOBAL_STORAGE[obj.id] = obj
    
    def get(self, obj_id):
        """Get object by ID from global storage"""
        return _GLOBAL_STORAGE.get(obj_id)
    
    def get_all(self):
        """Get all objects from global storage"""
        return list(_GLOBAL_STORAGE.values())
    
    def update(self, obj_id, data):
        """Update object in global storage"""
        obj = self.get(obj_id)
        if obj:
            obj.update(data)
            return obj
        return None
    
    def delete(self, obj_id):
        """Delete object from global storage"""
        if obj_id in _GLOBAL_STORAGE:
            del _GLOBAL_STORAGE[obj_id]
    
    def get_by_attribute(self, attr_name, attr_value):
        """Get object by attribute from global storage"""
        for obj in _GLOBAL_STORAGE.values():
            if getattr(obj, attr_name, None) == attr_value:
                return obj
        return None


class SQLAlchemyRepository(Repository):
    """SQLAlchemy-based repository implementation"""
    
    def __init__(self, model):
        """
        Initialize repository with a SQLAlchemy model.
        
        Args:
            model: SQLAlchemy model class
        """
        self.model = model
    
    def add(self, obj):
        """Add an object to the database"""
        # Import db locally to avoid circular import
        from hbnb.app import db
        db.session.add(obj)
        db.session.commit()
    
    def get(self, obj_id):
        """Get an object by ID"""
        # Import db locally to avoid circular import
        from hbnb.app import db
        return db.session.get(self.model, obj_id)
    
    def get_all(self):
        """Get all objects"""
        return self.model.query.all()
    
    def update(self, obj_id, data):
        """Update an object with new data"""
        # Import db locally to avoid circular import
        from hbnb.app import db
        obj = self.get(obj_id)
        if obj:
            for key, value in data.items():
                setattr(obj, key, value)
            db.session.commit()
            return obj
        return None
    
    def delete(self, obj_id):
        """Delete an object by ID"""
        # Import db locally to avoid circular import
        from hbnb.app import db
        obj = self.get(obj_id)
        if obj:
            db.session.delete(obj)
            db.session.commit()
    
    def get_by_attribute(self, attr_name, attr_value):
        """Get an object by a specific attribute"""
        return self.model.query.filter_by(**{attr_name: attr_value}).first()
