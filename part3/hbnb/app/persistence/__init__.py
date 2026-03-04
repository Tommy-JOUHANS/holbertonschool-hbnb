"""
Persistence layer initialization.
Provides repository selection based on configuration.
"""
import os
from hbnb.app.persistence.repository import InMemoryRepository, SQLAlchemyRepository


def get_repository(use_db=None):
    """
    Factory function to get the appropriate repository.
    
    Args:
        use_db: If True, use SQLAlchemy. If False, use InMemory. 
                If None, use environment variable.
    
    Returns:
        Repository class (not instance)
    """
    if use_db is None:
        use_db = os.getenv('USE_DATABASE', 'false').lower() == 'true'
    
    if use_db:
        return SQLAlchemyRepository
    else:
        return InMemoryRepository
