"""
Persistence layer package.

Provides access to repository implementations.
"""

from hbnb.app.persistence.repository import InMemoryRepository

__all__ = ["InMemoryRepository"]
